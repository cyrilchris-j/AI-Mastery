#!/usr/bin/env python3
"""
Day 4 · AI: Vectors - Teaching Meaning to Machines
Demonstrating sentence embeddings, cosine similarity, and cosine distance
using sentence-transformers, numpy, pandas, and seaborn.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

def run_vector_analysis():
    # Create Day-04 directory if it doesn't exist
    os.makedirs("Day-04", exist_ok=True)
    
    print("--- Day 4: Sentence Embeddings & Similarity ---")
    
    # 1. Define sentences
    sentences = [
        "It is a beautiful, sunny day outside.",                  # Weather 1
        "The weather is lovely and warm today.",                  # Weather 2 (Similar)
        "A software engineer is writing clean Python code.",        # Coding 1
        "The developer is programming in Python on their laptop.",  # Coding 2 (Similar)
        "A stray cat is sleeping soundly under the car."          # Irrelevant (Different)
    ]
    
    # 2. Load model
    print("\nLoading sentence-transformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Model loaded successfully!")
    
    # 3. Generate embeddings
    print("\nGenerating sentence embeddings...")
    embeddings = model.encode(sentences, convert_to_numpy=True)
    
    print(f"Number of sentences encoded: {len(embeddings)}")
    print(f"Embedding vector dimension: {embeddings.shape[1]}")
    
    # Show first 5 dimensions of each sentence embedding
    for i, (sentence, emb) in enumerate(zip(sentences, embeddings), 1):
        print(f"  Sentence {i} (first 5 dims): {emb[:5]}... (Truncated)")
        
    # 4. Compute Pairwise Cosine Similarity and Cosine Distance
    # Similarity matrix
    # cos_sim returns a tensor, we convert to numpy
    sim_matrix = cos_sim(embeddings, embeddings).numpy()
    
    # Cosine distance = 1 - cosine similarity
    dist_matrix = 1.0 - sim_matrix
    
    # 5. Build DataFrames for display
    sent_labels = [f"S{i}: {s[:30]}..." for i, s in enumerate(sentences, 1)]
    df_similarity = pd.DataFrame(sim_matrix, index=sent_labels, columns=sent_labels)
    df_distance = pd.DataFrame(dist_matrix, index=sent_labels, columns=sent_labels)
    
    print("\n=== Cosine Similarity Matrix (Higher is More Similar) ===")
    print(df_similarity.round(4))
    
    print("\n=== Cosine Distance Matrix (Lower is More Similar) ===")
    print(df_distance.round(4))
    
    # 6. Save Heatmap Visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df_similarity, 
        annot=True, 
        cmap="coolwarm", 
        vmin=-1.0, 
        vmax=1.0, 
        fmt=".4f", 
        linewidths=0.5,
        cbar_kws={'label': 'Cosine Similarity Score'}
    )
    plt.title("Sentence Embeddings Pairwise Cosine Similarity Heatmap", fontsize=14, fontweight='bold', pad=15)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    heatmap_path = "Day-04/similarity_heatmap.png"
    plt.savefig(heatmap_path, dpi=300)
    print(f"\n✓ Saved similarity heatmap to '{heatmap_path}'")
    plt.close()
    
    # 7. Print analysis of pairs
    print("\n=== Detailed Pairwise Comparison & Intuition Analysis ===")
    pairs_list = []
    
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            sim = sim_matrix[i, j]
            dist = dist_matrix[i, j]
            
            # Categorize the relationship
            if i in [0, 1] and j in [0, 1]:
                rel_type = "Weather Theme (Highly Similar)"
            elif i in [2, 3] and j in [2, 3]:
                rel_type = "Coding Theme (Highly Similar)"
            elif i == 4 or j == 4:
                rel_type = "Stray Cat Theme (Unrelated)"
            else:
                rel_type = "Cross-Theme (Unrelated)"
                
            pairs_list.append({
                "Pair": f"Sentence {i+1} & Sentence {j+1}",
                "Text 1": sentences[i],
                "Text 2": sentences[j],
                "Similarity": float(sim),
                "Distance": float(dist),
                "Type": rel_type
            })
            
            print(f"\nComparing:")
            print(f"  S{i+1}: \"{sentences[i]}\"")
            print(f"  S{j+1}: \"{sentences[j]}\"")
            print(f"  ↳ Cosine Similarity: {sim:.4f}")
            print(f"  ↳ Cosine Distance:   {dist:.4f}")
            print(f"  ↳ Category:          {rel_type}")
            
    # Save the results to a JSON file for markdown template ingestion
    results = {
        "sentences": sentences,
        "similarity_matrix": sim_matrix.tolist(),
        "distance_matrix": dist_matrix.tolist(),
        "pairwise_comparisons": pairs_list
    }
    
    with open("Day-04/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("✓ Successfully saved results to 'Day-04/results.json'")
    
if __name__ == "__main__":
    run_vector_analysis()
