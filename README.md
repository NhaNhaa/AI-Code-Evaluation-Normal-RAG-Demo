# AI-Code-Evaluation-Normal-RAG-Demo

This project demonstrates **Standard RAG (Normal RAG)** used for evaluating student code by comparing it with instructor code using **similarity search**, **chunking**, and **embeddings** stored inside a **FAISS vector database**.

> ⚠️ This demo evaluates by **similarity**, not by understanding logic or grading criteria.
> That is why Normal RAG is **not suitable** for real code evaluation.

---

## 📂 Project Structure

```
📦 Normal_RAG_demo
 ┣ 📂 instructor_code                 # Teacher’s reference solution
 ┃ ┣ 📂 components
 ┃ ┃ ┣ 📜 Footer.jsx                  # Instructor footer component
 ┃ ┃ ┣ 📜 Header.jsx                  # Instructor header component
 ┃ ┃ ┣ 📜 TodoItem.js                 # Instructor todo item logic
 ┃ ┃ ┗ 📜 TodoList.js                 # Instructor todo list logic
 ┃ ┣ 📂 utils
 ┃ ┃ ┗ 📜 helper.js                   # Instructor helper functions
 ┃ ┣ 📜 App.jsx                       # Instructor main React app
 ┃ ┗ 📜 index.js                      # Instructor entry point
 ┣ 📂 student_code                    # Student project submission
 ┃ ┣ 📂 components
 ┃ ┃ ┣ 📜 Footer.jsx                  # Student footer component
 ┃ ┃ ┣ 📜 Header.jsx                  # Student header component
 ┃ ┃ ┣ 📜 TodoItem.js                 # Student todo item logic
 ┃ ┃ ┗ 📜 TodoList.js                 # Student todo list logic
 ┃ ┣ 📂 utils
 ┃ ┃ ┗ 📜 helper.js                   # Student helper functions
 ┃ ┣ 📜 App.jsx                       # Student main React app
 ┃ ┗ 📜 index.js                      # Student entry point
 ┣ 📜 chunk_summary.txt               # Summary of all generated code chunks
 ┣ 📜 rag_agent.py                    # Step 3: evaluates similarity and generates feedback
 ┣ 📜 similarity_results.txt          # Output file from Step 2 (top matches)
 ┣ 📜 step1_chunk_embed.py            # Step 1: chunk + embed instructor code into FAISS
 ┣ 📜 step2_query.py                  # Step 2: compare student chunks with teacher chunks
 ┗ 📜 student_feedback.txt            # Final scoring and feedback for the student (Step 3)

```

---

# ⚙️ 1. Installation Guide

## ✔ Step 1 — Create virtual environment

```bash
python -m venv venv
```

## ✔ Step 2 — Activate it

### VScode:

```bash
source venv/Scripts/activate
```

### Mac / Linux:

```bash
source venv/bin/activate
```

## ✔ Step 3 — Install all dependencies

```bash
pip install -r requirements.txt
```

You do **not** need to install anything manually.
`requirements.txt` contains everything required.

---

# ▶️ 2. How to Run the Pipeline

### **Step 1 — Chunk + Embed instructor & student code**

This cuts the code into small pieces and stores embeddings into FAISS.

```bash
python step1_chunk_embed.py
```

Output includes:

* number of instructor files loaded
* number of student files loaded
* number of chunks produced
* FAISS database saved to folder: `faiss_demo/`

---

### **Step 2 — Query: Compare student vs instructor**

This loads FAISS and returns the most similar instructor chunks for each student chunk.

```bash
python step2_query.py
```

Output includes:

* preview of student chunks
* top-2 closest instructor chunks
* similarity comparison

---

### **Step 3 — Evaluate using simple RAG agent**

This applies a **dummy evaluator** to generate:

* feedback
* score (based on similarity)

```bash
python rag_agent.py
```

This is NOT a real evaluator — just a demo of how a RAG agent would work.

---

# 🧠 How Normal RAG Works (Short Summary)

1. **Teacher code** + **student code** → loaded
2. Code is **chunked** (ex: 300 characters per chunk)
3. Each chunk is **embedded** → converted into a vector
4. All vectors stored inside **FAISS**
5. Student chunks are searched against instructor chunks
6. Similarity determines:

   * what feedback is shown
   * what score is produced

Normal RAG does **not** understand code or logic.
It only measures **text similarity**, which is why it is *not suitable* for real grading.

---

# 📄 Requirements

Example of what your `requirements.txt` should contain:

```
langchain
langchain-community
langchain-text-splitters
faiss-cpu
numpy
```

(You may adjust based on your actual version.)

---

# 🎓 For Teachers

This demo shows why **normal RAG is not effective** for educational code evaluation:

* It cannot analyze logic
* It cannot detect errors
* It cannot apply scoring rubrics
* It only compares text similarity

For realistic evaluation, an **Agentic RAG system** is required.

---
