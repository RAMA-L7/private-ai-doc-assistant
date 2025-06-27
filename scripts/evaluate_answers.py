# evaluate_answers.py
# -------------------------------------------------
# Evaluation using semantic similarity (MiniLM embeddings)

import os
import pandas as pd
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer, util
from llama_cpp import Llama

# ---------- Paths ----------
CHROMA_DIR = "embeddings/chroma"
MODEL_PATH = "models/mistral-7b.Q4_0.gguf"

# ---------- Load Models ----------
print("🔠 Loading embedding models...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # for query/retrieval
similarity_model = SentenceTransformer("all-MiniLM-L6-v2")  # for scoring answers

print("📦 Connecting to ChromaDB...")
client = chromadb.Client(Settings(is_persistent=True, persist_directory=CHROMA_DIR))
collection = client.get_collection("documents")

print("🤖 Loading local Llama model...")
llm = Llama(model_path=MODEL_PATH, n_ctx=4096, n_threads=8)

# ---------- Ask Assistant ----------
def query_assistant(question: str) -> str:
    query_embedding = embedder.encode([question]).tolist()[0]
    results = collection.query(query_embeddings=[query_embedding], n_results=7)

    context = "\n\n".join(results["documents"][0])
    prompt = f"""
You are a precise assistant that answers using only the given document context.
If the answer is not found in the context, say: "I don’t have that information."
Be concise and accurate.

Context:
{context}

Question: {question}
Answer:"""

    response = llm(prompt=prompt, max_tokens=512, stop=["\n\n", "</s>"])
    return response["choices"][0]["text"].strip()

# ---------- Q&A Ground Truth ----------
qa_pairs = [
    {
        "question": "What does SmartAudit AI do?",
        "expected": "SmartAudit AI helps fintech startups audit transactions in real-time using LLMs. It detects anomalies via pattern learning, integrates with banking APIs (Plaid, Yodlee), and delivers explainable reports for compliance."
    },
    {
        "question": "Who are the target users of SmartAudit AI?",
        "expected": "Fintech CTOs, auditors, and regulators."
    },
    {
        "question": "What is the projected RegTech market size?",
        "expected": "$21B by 2027."
    },
    {
        "question": "How much funding is being asked for?",
        "expected": "$1M seed funding."
    },
    {
        "question": "What business model is used?",
        "expected": "SaaS subscription model."
    },
    {
        "question": "What is the audit API endpoint?",
        "expected": "/audit/transactions"
    },
    {
        "question": "What does the API response contain?",
        "expected": "It contains an audit_score and a list of flags such as suspicious_vendor or duplicate_entry."
    },
    {
        "question": "What are the company’s cultural values?",
        "expected": "Think customer-first, move fast, stay grounded, document what you learn."
    },
    {
        "question": "What is step 1 of onboarding?",
        "expected": "GitHub access and repo clone."
    },
    {
        "question": "What model was evaluated?",
        "expected": "Mistral-7B-Instruct."
    },
    {
        "question": "What hallucination rate was reported?",
        "expected": "5.2%"
    },
    {
        "question": "What is the conclusion from the eval report?",
        "expected": "Mistral-7B-Instruct offers the best balance for edge deployment."
    }
]

# ---------- Evaluation ----------
def evaluate(qa_pairs):
    rows = []
    for qa in qa_pairs:
        question = qa["question"]
        expected = qa["expected"]
        assistant_answer = query_assistant(question)

        # Semantic similarity (cosine between embeddings)
        emb_expected = similarity_model.encode(expected, convert_to_tensor=True)
        emb_answer = similarity_model.encode(assistant_answer, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(emb_expected, emb_answer).item()

        rows.append({
            "Question": question,
            "Expected": expected,
            "Assistant": assistant_answer,
            "Similarity": round(similarity, 2),
            "Pass": "✅" if similarity >= 0.75 else "❌"
        })
    return pd.DataFrame(rows)

# ---------- Run ----------
df = evaluate(qa_pairs)

# ---------- Output ----------
print("\n=== Evaluation Results ===")
print(df.to_string(index=False))

csv_path = "evaluation_results_semantic.csv"
df.to_csv(csv_path, index=False)
print(f"\n📄 Results saved to {csv_path}")
