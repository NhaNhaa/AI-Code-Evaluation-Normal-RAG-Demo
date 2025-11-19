import os
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# ---------- Dummy Embeddings (callable now) ----------
class DummyEmbeddings:
    """Dummy embeddings for testing FAISS retrieval."""
    
    def embed_documents(self, docs):
        return [np.random.rand(768).tolist() for _ in docs]

    def embed_query(self, query):
        return np.random.rand(768).tolist()

    # Make it callable so FAISS works correctly
    def __call__(self, text):
        return self.embed_query(text)

# ---------- Config ----------
STUDENT_CODE_DIR = "./student_code"
FAISS_FOLDER = "./faiss_demo"

CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

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

print("📌 Loading student code...")
student_codes = load_code(STUDENT_CODE_DIR)
print(f"✅ Loaded {len(student_codes)} student files.")

# ---------- Split student code into chunks ----------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
)
student_chunks = text_splitter.split_text("\n".join(student_codes))
print(f"📌 Student chunks: {len(student_chunks)}")

# ---------- Load FAISS vector store ----------
embeddings = DummyEmbeddings()
print("📌 Loading FAISS index...")
vector_store = FAISS.load_local(
    FAISS_FOLDER,
    embeddings,
    allow_dangerous_deserialization=True
)
print("✅ FAISS index loaded successfully!")

# ---------- Perform similarity search and save to file ----------
with open("similarity_results.txt", "w", encoding="utf-8") as f:
    for i, chunk in enumerate(student_chunks[:5]):  # preview first 5 chunks
        f.write(f"==============================\n")
        f.write(f"🔎 Student Chunk #{i+1}\n")
        f.write("==============================\n")
        f.write(chunk + "\n\n")

        results = vector_store.similarity_search(chunk, k=2)

        f.write("📌 Closest Instructor Chunks:\n")
        for idx, doc in enumerate(results):
            f.write(f"\n--- Match #{idx+1} ---\n")
            f.write(doc.page_content[:500] + "\n")  # preview first 500 chars

        f.write("\n\n")

print("💾 Similarity results saved to similarity_results.txt")
