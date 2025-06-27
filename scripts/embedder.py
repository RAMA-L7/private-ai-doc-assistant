# scripts/embedder.py

import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer
from uuid import uuid4

# 🔧 Configuration
DATA_DIR = "data"
EMBED_DIR = "embeddings"
CHROMA_DIR = os.path.join(EMBED_DIR, "chroma")
os.makedirs(CHROMA_DIR, exist_ok=True)

# 📌 Load embedding model
print("🔠 Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# 🧠 Connect to ChromaDB (new syntax)
print("📦 Connecting to ChromaDB...")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name="documents")

# 📂 Read and embed PDFs
def process_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() or ""
    return full_text

def chunk_text(text, chunk_size=700, overlap=150):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

print("📄 Reading PDFs from /data...")
for file in os.listdir(DATA_DIR):
    if file.endswith(".pdf"):
        filepath = os.path.join(DATA_DIR, file)
        print(f"📘 Processing: {file}")
        raw_text = process_pdf(filepath)
        chunks = chunk_text(raw_text)

        embeddings = embedder.encode(chunks).tolist()
        ids = [str(uuid4()) for _ in chunks]

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": file}] * len(chunks)
        )

# 💾 Persist DB
print("💾 Saving DB...")
print("✅ Embedding and storage complete.")
