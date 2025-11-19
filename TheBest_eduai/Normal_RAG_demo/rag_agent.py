import os
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# ---------- Dummy Embeddings ----------
class DummyEmbeddings:
    """Dummy embeddings for FAISS."""
    
    def embed_documents(self, docs):
        return [np.random.rand(768).tolist() for _ in docs]

    def embed_query(self, query):
        return np.random.rand(768).tolist()

    def __call__(self, text):
        return self.embed_query(text)

# ---------- Config ----------
STUDENT_CODE_DIR = "./student_code"
FAISS_FOLDER = "./faiss_demo"
FEEDBACK_FILE = "student_feedback.txt"

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

# ---------- Rubric ----------
RUBRIC = {
    "App component implemented": 25,
    "Header/Footer implemented": 20,
    "TodoList functionality": 30,
    "PropTypes and helpers": 15,
    "Code style / exports": 10
}

# ---------- Load student code ----------
def load_code(folder_path):
    code_texts = []
    if not os.path.exists(folder_path):
        print(f"❌ Error: Directory not found — {folder_path}")
        return []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".js") or file.endswith(".jsx"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code_texts.append(f.read())
                except Exception as e:
                    print(f"❌ Could not read file {file}: {e}")
    return code_texts

# ---------- Split student code ----------
def split_code(texts):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_text("\n".join(texts))

# ---------- Simple rubric evaluator ----------
def evaluate_chunk(chunk):
    score = 0
    feedback_items = []

    # Check for App component
    if "function App" in chunk or "const App" in chunk:
        score += RUBRIC["App component implemented"]
    else:
        feedback_items.append("Missing App component.")

    # Check Header/Footer usage
    if "Header" in chunk and "Footer" in chunk:
        score += RUBRIC["Header/Footer implemented"]
    else:
        feedback_items.append("Header or Footer not used properly.")

    # Check TodoList
    if "TodoList" in chunk:
        score += RUBRIC["TodoList functionality"]
    else:
        feedback_items.append("TodoList functionality missing.")

    # Check PropTypes or helper usage
    if "PropTypes" in chunk or "formatMessage" in chunk:
        score += RUBRIC["PropTypes and helpers"]
    else:
        feedback_items.append("PropTypes or helper functions missing.")

    # Check for export statement
    if "export" in chunk:
        score += RUBRIC["Code style / exports"]
    else:
        feedback_items.append("Missing export statement.")

    return score, feedback_items

# ---------- Main Evaluator ----------
def evaluate_student_project():
    print("📌 Loading student code...")
    student_codes = load_code(STUDENT_CODE_DIR)
    print(f"✅ Loaded {len(student_codes)} student files.")

    student_chunks = split_code(student_codes)
    print(f"📌 Student chunks: {len(student_chunks)}")

    print("📌 Loading FAISS index...")
    embeddings = DummyEmbeddings()
    vector_store = FAISS.load_local(
        FAISS_FOLDER,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("✅ FAISS index loaded successfully!")

    all_results = []

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        f.write("===== Student Project Feedback =====\n\n")

        for i, chunk in enumerate(student_chunks):
            f.write(f"==============================\n")
            f.write(f"🔎 Student Chunk #{i+1}\n")
            f.write(f"==============================\n")
            f.write(chunk[:500] + "\n\n")  # preview

            # Step 2: FAISS retrieval for reference
            closest_instructor_chunks = vector_store.similarity_search(chunk, k=3)

            # Rubric evaluation
            score, feedback_items = evaluate_chunk(chunk)
            f.write("📌 Score for this chunk: {}\n".format(score))
            f.write("📌 Feedback:\n")
            if feedback_items:
                for item in feedback_items:
                    f.write("- " + item + "\n")
            else:
                f.write("- Excellent work!\n")

            # Optional: Show top 1 FAISS match for context
            f.write("\n📌 Closest Instructor Chunk (preview):\n")
            if closest_instructor_chunks:
                f.write(closest_instructor_chunks[0].page_content[:300] + "\n")
            f.write("\n\n")

            all_results.append(score)

        # Final project score
        final_score = int(np.mean(all_results))
        f.write("==============================\n")
        f.write(f"🏆 Final Project Score: {final_score}/100\n")
        f.write("==============================\n")

    print(f"✅ Evaluation completed. Feedback saved in {FEEDBACK_FILE}")

# ---------- Run ----------
if __name__ == "__main__":
    evaluate_student_project()
