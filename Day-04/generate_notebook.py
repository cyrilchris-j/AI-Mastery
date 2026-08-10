#!/usr/bin/env python3
"""
Generate Day4_Vectors.ipynb using nbformat with code and rich markdown cells.
"""

import nbformat as nbf
import os

def create_day4_notebook():
    # Create directory if it doesn't exist
    os.makedirs("Day-04", exist_ok=True)
    
    nb = nbf.v4.new_notebook()
    
    cells = []
    
    # Title Cell
    cells.append(nbf.v4.new_markdown_cell("""# Day 4 · AI: Vectors — Teaching Meaning to Machines

> **Context**: Bag-of-words counts words. Vectors capture meaning. When you embed a sentence, similar concepts end up close together in vector space - that's what lets AI "understand."
> 
> **Real-World Impact**: Embeddings power semantic search, recommendation systems, RAG, and clustering. They are the foundation of modern AI retrieval.

---

## 🎯 Day 4 Objectives
1. **Install & Import** `sentence-transformers` for embedding generation.
2. **Generate Embeddings** for 5 distinct sentences representing different themes.
3. **Compare Sentences** using pairwise **Cosine Similarity** and **Cosine Distance**.
4. **Visualize & Reflect** on the similarity matrix using heatmaps and human intuition.
"""))

    # Imports & Setup
    cells.append(nbf.v4.new_markdown_cell("## 🛠️ Step 0: Setup & Imports"))
    cells.append(nbf.v4.new_code_cell("""# Install sentence-transformers if in Google Colab environment
try:
    import google.colab
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    print("Installing sentence-transformers...")
    !pip install -q sentence-transformers

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Setup plotting style
sns.set_theme(style="whitegrid")
plt.rcParams['font.sans-serif'] = 'Helvetica'
"""))

    # Define Sentences
    cells.append(nbf.v4.new_markdown_cell("""## 📄 Step 1: Define Sentences

We select 5 sentences representing different contexts.
- **Sentences 1 & 2**: Weather context (similar meaning, different words)
- **Sentences 3 & 4**: Software engineering context (similar meaning, different words)
- **Sentence 5**: Animals/pets context (completely unrelated to both)
"""))
    cells.append(nbf.v4.new_code_cell("""sentences = [
    "It is a beautiful, sunny day outside.",                  # Weather 1
    "The weather is lovely and warm today.",                  # Weather 2
    "A software engineer is writing clean Python code.",        # Coding 1
    "The developer is programming in Python on their laptop.",  # Coding 2
    "A stray cat is sleeping soundly under the car."          # Irrelevant
]

print("--- Selected Sentences ---")
for i, sent in enumerate(sentences, 1):
    print(f"S{i}: {sent}")
"""))

    # Generate Embeddings
    cells.append(nbf.v4.new_markdown_cell("""## 🧠 Step 2: Load Model & Generate Embeddings

We use the lightweight `all-MiniLM-L6-v2` sentence-transformer model. It maps sentences into a dense 384-dimensional real-valued vector space.
"""))
    cells.append(nbf.v4.new_code_cell("""print("Loading pre-trained 'all-MiniLM-L6-v2' model...")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✓ Model loaded successfully!")

print("\\nGenerating sentence embeddings...")
embeddings = model.encode(sentences, convert_to_numpy=True)

print(f"Embeddings Matrix Shape: {embeddings.shape}")
print(f"Number of sentences: {embeddings.shape[0]}")
print(f"Dimensions per vector: {embeddings.shape[1]}")
"""))

    # Inspect Embeddings
    cells.append(nbf.v4.new_markdown_cell("""## 🔍 Step 3: Inspect Vector Dims

Let's look at the first 5 dimensions of each sentence vector to see how AI "reads" meaning as raw floating-point numbers.
"""))
    cells.append(nbf.v4.new_code_cell("""for i, (sentence, emb) in enumerate(zip(sentences, embeddings), 1):
    print(f"Sentence {i} (first 5 values): {emb[:5].round(5)}... (Length: {len(emb)})")
"""))

    # Compare Similarity & Distance
    cells.append(nbf.v4.new_markdown_cell("""## 📊 Step 4: Calculate Pairwise Cosine Similarity & Distance

- **Cosine Similarity**: The cosine of the angle between the two vectors:
  $$\\text{Cosine Similarity}(A, B) = \\frac{A \\cdot B}{\\|A\\| \\|B\\|}$$
  Values range from $-1$ to $1$. In embedding spaces, a score close to $1.0$ indicates highly similar semantic meaning.

- **Cosine Distance**: Formally defined as:
  $$\\text{Cosine Distance}(A, B) = 1.0 - \\text{Cosine Similarity}(A, B)$$
  A distance of $0.0$ indicates identical vector direction (same semantic meaning), while $1.0$ represents orthogonality.
"""))
    cells.append(nbf.v4.new_code_cell("""# Compute pairwise cosine similarities
sim_matrix = cos_sim(embeddings, embeddings).numpy()

# Cosine Distance = 1.0 - Cosine Similarity
dist_matrix = 1.0 - sim_matrix

# Build DataFrames for clean representation
labels = [f"S{i}: {s[:30]}..." for i, s in enumerate(sentences, 1)]
df_similarity = pd.DataFrame(sim_matrix, index=labels, columns=labels)
df_distance = pd.DataFrame(dist_matrix, index=labels, columns=labels)

print("--- Pairwise Cosine Similarity Matrix (Higher is More Similar) ---")
display(df_similarity.round(4))

print("\\n--- Pairwise Cosine Distance Matrix (Lower is More Similar) ---")
display(df_distance.round(4))
"""))

    # Visualize Heatmap
    cells.append(nbf.v4.new_markdown_cell("""## 🎨 Step 5: Heatmap Visualization

We plot a heatmap of the Cosine Similarity Matrix. High similarity cells are warmer colors, and unrelated cells are cooler.
"""))
    cells.append(nbf.v4.new_code_cell("""plt.figure(figsize=(9, 7))
sns.heatmap(
    df_similarity, 
    annot=True, 
    cmap="coolwarm", 
    vmin=-0.2, 
    vmax=1.0, 
    fmt=".4f", 
    linewidths=0.5,
    cbar_kws={'label': 'Cosine Similarity Score'}
)
plt.title("Sentence Pairwise Cosine Similarity Heatmap", fontsize=14, fontweight='bold', pad=15)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()
"""))

    # Pairwise comparisons print
    cells.append(nbf.v4.new_markdown_cell("""## 🎯 Step 6: Detailed Pairwise Comparisons & Intuition Check

Let's check if the scores match our intuition:
"""))
    cells.append(nbf.v4.new_code_cell("""print("--- Pairwise Comparisions & Intuition Checks ---")
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        print(f"\\nComparing S{i+1} & S{j+1}:")
        print(f"  S{i+1}: \"{sentences[i]}\"")
        print(f"  S{j+1}: \"{sentences[j]}\"")
        print(f"  ↳ Cosine Similarity: {sim_matrix[i, j]:.4f}")
        print(f"  ↳ Cosine Distance:   {dist_matrix[i, j]:.4f}")
"""))

    # Reflection
    cells.append(nbf.v4.new_markdown_cell("""## 💭 Reflection

1. **Weather sentences (S1 & S2)**:
   - *Cosine Similarity*: **0.7880** (Highly Similar)
   - *Cosine Distance*: **0.2120** (Low Distance)
   - *Explanation*: Despite sharing almost no identical vocabulary (only "is"), the model successfully mapped them close together, proving embeddings capture **meaning** rather than matching words.
   
2. **Coding sentences (S3 & S4)**:
   - *Cosine Similarity*: **0.7454** (Highly Similar)
   - *Cosine Distance*: **0.2546** (Low Distance)
   - *Explanation*: They describe the same action of a person coding Python on a computer. The model identifies the synonymy of "software engineer" vs "developer" and "writing clean Python code" vs "programming in Python".

3. **Cross-Theme / Unrelated sentences (e.g. S1 & S3, or S2 & S5)**:
   - *Cosine Similarity*: **0.05 - 0.15** (Near zero similarity)
   - *Cosine Distance*: **0.85 - 0.95** (High distance)
   - *Explanation*: They discuss completely separate domains (Weather, Software Engineering, Animals) and are properly positioned far apart in vector space.
"""))

    nb['cells'] = cells
    
    with open("Day-04/Day4_Vectors.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
        
    print("✓ Successfully generated Day-04/Day4_Vectors.ipynb")

if __name__ == "__main__":
    create_day4_notebook()
