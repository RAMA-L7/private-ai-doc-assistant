# scripts/chat_engine.py
import chromadb
import streamlit as st                      # ← needed for @st.cache_resource
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama
from typing import List

# ── Configuration ────────────────────────────────────────────────────────────
CHROMA_DIR = "embeddings/chroma"
MODEL_PATH = "models/mistral-7b.Q4_0.gguf"   # adjust if your filename differs

# ── Cached loaders (load once, reuse) ────────────────────────────────────────
@st.cache_resource
def load_embedder():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_llm():
    return Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=6,     # adjust to CPU cores
        n_batch=8,
        verbose=False
    )

# Instantiate cached objects
embedder = load_embedder()
llm       = load_llm()

# ── ChromaDB client (persistent) ─────────────────────────────────────────────
client      = chromadb.PersistentClient(path=CHROMA_DIR)
collection  = client.get_or_create_collection("documents")

# ── Helper: vector search ────────────────────────────────────────────────────
def _search_docs(query: str, top_k: int = 4) -> List[str]:
    q_vec   = embedder.encode([query])[0].tolist()
    result  = collection.query(query_embeddings=[q_vec], n_results=top_k)
    return result["documents"][0] if result["documents"] else []

# ── Helper: trim context to fit model window ─────────────────────────────────
def trim_context(docs, max_chars=3000) -> str:
    ctx = "\n\n".join(docs)
    return ctx[:max_chars] if len(ctx) > max_chars else ctx

# ── Public: generate answer ─────────────────────────────────────────────────
def generate_answer(query: str) -> str:
    try:
        docs = _search_docs(query, top_k=4)
        if not docs:
            return "I couldn't find relevant information in the uploaded documents."

        context = trim_context(docs)

        prompt = f"""You are a helpful assistant. Use ONLY the following context to answer the question.
If the answer is not found in the context, say: "I don't have that information."

Context:
{context}

Question: {query}
Answer:"""

        resp = llm(prompt=prompt, max_tokens=512, stop=["</s>", "Context:", "Question:"])
        return resp["choices"][0]["text"].strip().replace("\n", " ").replace("  ", " ")

    except Exception as e:
        return f"Error while generating answer: {e}"
