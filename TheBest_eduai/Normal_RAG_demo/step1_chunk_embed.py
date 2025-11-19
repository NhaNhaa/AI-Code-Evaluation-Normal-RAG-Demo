import os
import numpy as np

# --- Correct imports for LangChain 1.0.7 ---
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# ---------- Dummy Embeddings (for demo/testing) ----------
class DummyEmbeddings:
    """A dummy class to simulate an embedding model."""
    def embed_documents(self, docs):
        return [np.random.rand(768).tolist() for _ in docs]

    def embed_query(self, query):
        return np.random.rand(768).tolist()

# ---------- Config ----------
INSTRUCTOR_CODE_DIR = "./instructor_code"
STUDENT_CODE_DIR = "./student_code"

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

IGNORE_FOLDERS = ['node_modules', '.git', '__pycache__']
IGNORE_FILES = ['package-lock.json', 'package.json', 'eslint.config.js']

# ---------- Step 1: Load code files ----------
def load_code(folder_path):
    code_texts = []

    if not os.path.exists(folder_path):
        print(f"❌ Error: Directory not found — {folder_path}")
        return []

    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if d not in IGNORE_FOLDERS]

        for file in files:
            if file in IGNORE_FILES:
                continue
            if file.endswith(".js") or file.endswith(".jsx"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        code_texts.append(f.read())
                except Exception as e:
                    print(f"❌ Could not read file {file}: {e}")

    return code_texts

print("📌 Loading code files...")

instructor_codes = load_code(INSTRUCTOR_CODE_DIR)
student_codes = load_code(STUDENT_CODE_DIR)

print(f"✅ Loaded {len(instructor_codes)} instructor files.")
print(f"✅ Loaded {len(student_codes)} student files.")

# ---------- Step 2: Chunk the code ----------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)

if instructor_codes:
    instructor_chunks = text_splitter.split_text("\n".join(instructor_codes))
    student_chunks = text_splitter.split_text("\n".join(student_codes))

    print(f"📌 Instructor chunks: {len(instructor_chunks)}")
    print(f"📌 Student chunks: {len(student_chunks)}")

    embeddings = DummyEmbeddings()

    vector_store = FAISS.from_texts(
        instructor_chunks,
        embeddings
    )

    vector_store.save_local("faiss_demo")
    print("💾 FAISS vector store saved to: faiss_demo")

else:
    print("⚠️ No instructor code found — skipping FAISS creation.")

with open("chunk_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Loaded {len(instructor_codes)} instructor files.\n")
    f.write(f"Loaded {len(student_codes)} student files.\n")
    f.write(f"Instructor chunks: {len(instructor_chunks) if instructor_codes else 0}\n")
    f.write(f"Student chunks: {len(student_chunks) if instructor_codes else 0}\n")
print("💾 Summary saved to chunk_summary.txt")
