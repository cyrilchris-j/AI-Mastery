# Day 02: Your First Python AI Script

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cyrilchris-j/60daysclaude/blob/main/Day-02/Day_02_Your_First_Python_AI_Script.ipynb)

> **Context:** You don't need to master Python to build AI. You just need to run it. Comfort comes from doing.
> 
> **Real-World Impact:** Every AI engineer ships code in Python. Getting comfortable with notebooks and basic text operations is the foundation for tokenization, prompt engineering, and building LLM pipelines.

---

## 🎯 Learning Objectives

- Set up a Google Colab notebook environment and run Python interactively.
- Build a Python script that tokenizes input sentences and computes word frequency statistics.
- Implement a text cleaning and normalization pipeline (stripping punctuation, converting to lowercase, and collapsing irregular whitespace).

---

## 💻 Notebook Structure & Functional Cells

The Jupyter Notebook [`Day_02_Your_First_Python_AI_Script.ipynb`](./Day_02_Your_First_Python_AI_Script.ipynb) consists of **3 main functional code cells**:

### 1. Cell 1: Environment Setup & First Python Execution
- **Purpose:** Verifies Python version and runtime environment in Google Colab.
- **Key Concepts:** System module, basic execution output, string formatting.

```python
import sys

print("🚀 Hello, World! Welcome to Day 2 of the 60 Days of AI Challenge!")
print(f"Python Version: {sys.version.split()[0]}")
print("Status: Environment initialized and ready for AI text processing.")
```

### 2. Cell 2: Sentence Word Frequency Counter
- **Purpose:** Reads an input sentence, strips punctuation, converts tokens to lowercase, and calculates word frequencies.
- **Key Concepts:** `str.translate`, `string.punctuation`, list comprehensions, `collections.Counter`.

```python
from collections import Counter
import string

def count_word_frequency(sentence: str) -> dict[str, int]:
    translator = str.maketrans('', '', string.punctuation)
    clean_sentence = sentence.translate(translator)
    words = [word.lower() for word in clean_sentence.split()]
    return dict(Counter(words))
```

### 3. Cell 3: Text Cleaning & Normalization Pipeline
- **Purpose:** Preprocesses messy text by lowercasing, stripping punctuation, and normalizing irregular whitespace (tabs, newlines, multiple spaces) into clean single-spaced text.
- **Key Concepts:** Regular expressions (`re.sub`), string cleaning, text normalization for NLP/LLM ingestion.

```python
import re
import string

def clean_text(input_text: str) -> str:
    text = input_text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    cleaned = re.sub(r'\s+', ' ', text).strip()
    return cleaned
```

---

## 🚀 How to Run

1. **Google Colab:** Click the **Open in Colab** badge above or open [Day_02_Your_First_Python_AI_Script.ipynb](./Day_02_Your_First_Python_AI_Script.ipynb) directly in Google Colab.
2. **Local Jupyter / VS Code:**
   ```bash
   jupyter notebook Day-02/Day_02_Your_First_Python_AI_Script.ipynb
   ```
