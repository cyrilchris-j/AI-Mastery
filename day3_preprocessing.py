#!/usr/bin/env python3
"""
Day 3 · AI: Text is Data - Turning Words into Numbers
Preprocessing pipeline demonstrating Tokenization, Stop Word & Punctuation Removal,
and Bag-of-Words (BoW) vectorization using NLTK, spaCy, and Scikit-Learn.
"""

import string
import json
import pandas as pd
import numpy as np

# NLP Libraries
import ssl
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

import spacy
from sklearn.feature_extraction.text import CountVectorizer

def initialize_nlp():
    """Ensure required NLTK resources and spaCy model are available."""
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
        
    nlp = spacy.load("en_core_web_sm")
    return nlp

def tokenize_text(text, nlp):
    """
    Tokenize text using both NLTK and spaCy.
    Returns a dictionary with sentence tokens and word tokens.
    """
    # NLTK Tokenization
    nltk_sentences = sent_tokenize(text)
    nltk_words = word_tokenize(text)
    
    # spaCy Tokenization
    doc = nlp(text)
    spacy_sentences = [sent.text for sent in doc.sents]
    spacy_words = [token.text for token in doc]
    
    return {
        "nltk_sentences": nltk_sentences,
        "nltk_words": nltk_words,
        "spacy_sentences": spacy_sentences,
        "spacy_words": spacy_words
    }

def remove_stopwords_and_punctuation(tokens):
    """
    Remove stop words and punctuation from a token list using NLTK & string.punctuation.
    Normalizes text by lowercasing.
    """
    stop_words = set(stopwords.words('english'))
    punctuation_set = set(string.punctuation)
    
    cleaned_tokens = []
    removed_items = []
    
    for token in tokens:
        clean_tok = token.lower()
        if clean_tok in punctuation_set:
            removed_items.append((token, "Punctuation"))
        elif clean_tok in stop_words:
            removed_items.append((token, "Stop Word"))
        elif not clean_tok.isalnum():
            removed_items.append((token, "Non-alphanumeric"))
        else:
            cleaned_tokens.append(clean_tok)
            
    return cleaned_tokens, removed_items

def remove_stopwords_spacy(text, nlp):
    """
    Remove stop words and punctuation using spaCy's native attributes (is_stop, is_punct).
    """
    doc = nlp(text)
    cleaned_tokens = [
        token.lemma_.lower() for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space and token.is_alpha
    ]
    return cleaned_tokens

def build_bag_of_words_custom(corpus_tokens):
    """
    Manual implementation of Bag-of-Words representation.
    1. Build Vocabulary set across all documents.
    2. Convert each document's tokens into a term-frequency vector.
    """
    # Step 1: Unique vocabulary (sorted for consistency)
    vocab = sorted(list(set(word for doc in corpus_tokens for word in doc)))
    word_to_idx = {word: idx for idx, word in enumerate(vocab)}
    
    # Step 2: Build document vector matrix
    bow_matrix = []
    for doc in corpus_tokens:
        vector = [0] * len(vocab)
        for word in doc:
            if word in word_to_idx:
                vector[word_to_idx[word]] += 1
        bow_matrix.append(vector)
        
    return vocab, word_to_idx, np.array(bow_matrix)

def build_bag_of_words_sklearn(corpus_clean_text):
    """
    Scikit-Learn CountVectorizer implementation of Bag-of-Words.
    """
    vectorizer = CountVectorizer()
    bow_sparse = vectorizer.fit_transform(corpus_clean_text)
    feature_names = vectorizer.get_feature_names_out()
    bow_dense = bow_sparse.toarray()
    
    return feature_names, bow_dense, vectorizer

def generate_dataset():
    """Build the dataset, perform preprocessing steps, and save preprocessed_dataset.csv."""
    nlp = initialize_nlp()
    
    raw_documents = [
        "Machines don't read words. They read numbers. Preprocessing is the first transformation that turns raw human language into something a model can learn from!",
        "Every NLP system - search engines, chatbots, text classification - starts with tokenization and text preprocessing. Get this wrong and the rest of the pipeline collapses.",
        "Tokenization breaks paragraphs into sentences and words, removing stop words like 'is', 'the', and 'and', along with punctuation marks.",
        "Bag-of-Words converts cleaned text tokens into numerical vectors representing word frequency counts for machine learning algorithms."
    ]
    
    dataset_rows = []
    corpus_cleaned_tokens = []
    corpus_cleaned_text_strings = []
    
    for i, raw_text in enumerate(raw_documents, 1):
        doc_id = f"Doc_{i}"
        
        # Step 1: Tokenize
        tokens_info = tokenize_text(raw_text, nlp)
        nltk_words = tokens_info["nltk_words"]
        
        # Step 2: Remove Stop Words & Punctuation
        cleaned_tokens, removed_info = remove_stopwords_and_punctuation(nltk_words)
        spacy_cleaned_tokens = remove_stopwords_spacy(raw_text, nlp)
        
        cleaned_text_str = " ".join(cleaned_tokens)
        corpus_cleaned_tokens.append(cleaned_tokens)
        corpus_cleaned_text_strings.append(cleaned_text_str)
        
        dataset_rows.append({
            "doc_id": doc_id,
            "raw_text": raw_text,
            "raw_token_count": len(nltk_words),
            "nltk_tokens": json.dumps(nltk_words),
            "spacy_tokens": json.dumps(tokens_info["spacy_words"]),
            "cleaned_token_count": len(cleaned_tokens),
            "cleaned_tokens": json.dumps(cleaned_tokens),
            "spacy_lemmatized_tokens": json.dumps(spacy_cleaned_tokens),
            "cleaned_text": cleaned_text_str
        })
        
    df = pd.DataFrame(dataset_rows)
    
    # Step 3: Bag-of-Words Matrix
    vocab, word_to_idx, custom_bow_matrix = build_bag_of_words_custom(corpus_cleaned_tokens)
    feature_names, bow_dense, vectorizer = build_bag_of_words_sklearn(corpus_cleaned_text_strings)
    
    # Add BoW representation as JSON vector to DataFrame
    df["bow_vector"] = [json.dumps(row.tolist()) for row in bow_dense]
    
    # Add individual word frequency columns for ML inspection
    bow_df = pd.DataFrame(bow_dense, columns=[f"bow_{word}" for word in feature_names])
    final_df = pd.concat([df, bow_df], axis=1)
    
    # Save CSV
    final_df.to_csv("preprocessed_dataset.csv", index=False)
    print("✓ Successfully saved preprocessed_dataset.csv")
    
    return final_df, vocab, custom_bow_matrix, feature_names, bow_dense

if __name__ == "__main__":
    print("--- Day 3: Text is Data Pipeline Execution ---")
    final_df, vocab, custom_bow_matrix, feature_names, bow_dense = generate_dataset()
    print(f"Dataset shape: {final_df.shape}")
    print(f"Vocabulary size: {len(feature_names)} unique words")
    print(f"Vocabulary list: {list(feature_names)[:10]}...")
