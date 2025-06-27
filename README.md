# 🧠 Private AI Document Assistant

A fully offline AI-powered assistant that helps you **ask natural language questions from your internal PDF documents**. Built for startups and teams that prioritize **data privacy**, **speed**, and **full control** — no cloud required.

---

## 🚀 Features

- 🔒 **Private & Offline**: No API keys, no external servers — runs 100% locally
- 📄 **PDF Ingestion**: Upload or use preloaded documents from the `data/` folder
- 🔍 **Smart Embeddings**: Uses `sentence-transformers` for accurate context search
- 🧠 **LLM Answering**: Uses Mistral 7B (or similar) via `llama-cpp-python`
- 🗂️ **Chat History Logging**: Saves Q&A logs with timestamps
- 🖼️ **Streamlit UI**: Intuitive, clean frontend for easy use
- 🧱 **Modular Structure**: Easy to extend and integrate

---

## 🧠 Tech Stack

| Component       | Tool / Library              |
|----------------|-----------------------------|
| Embeddings      | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector DB       | `ChromaDB` (local)          |
| PDF Parsing     | `pdfplumber`                |
| LLM             | `llama-cpp-python` + `mistral-7b.Q4_0.gguf` |
| Frontend        | `Streamlit`                 |
| Logging         | JSON-based log files        |

---

## 📁 Folder Structure

```
private-ai-doc-assistant/
├── app.py                      ← Main Streamlit app
├── data/                       ← Drop your PDFs here
├── embeddings/
│   └── chroma/                 ← Vector database folder
├── models/
│   └── mistral-7b.Q4_0.gguf    ← Local LLM file
├── scripts/
│   ├── chat_engine.py          ← Handles retrieval + LLM response
│   ├── chat_history.py         ← Saves interaction logs
│   └── upload_and_embed.py     ← Ingest + embed new PDFs (optional)
├── chat_logs/                  ← Timestamped JSON Q&A logs
├── README.md                   ← You're here
```

---

## 🧪 How to Run

> 📝 Prerequisite: Python 3.10+, and a machine capable of running a quantized model locally (e.g., Mistral or LLaMA)


1. **Install dependencies**
  ```bash
pip install -r requirements.txt

 Add your PDF files
  Drop your PDFs into the data/ folder

 Download a compatible LLM model
  Place a .gguf file (like mistral-7b.Q4_0.gguf) into the models/ folder
  You can get Mistral from huggingface.co/TheBloke

 Run the app
  streamlit run app.py

✨ Sample Use Case
“Who are the target users of SmartAudit AI?”
Answer: "The target users of SmartAudit AI are Fintech CTOs, auditors, and regulators."

📄 License
This project is open source under the MIT License.

🙌 Acknowledgements

- [Sentence Transformers](https://www.sbert.net/)
- [ChromaDB](https://www.trychroma.com/)
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
- [Streamlit](https://streamlit.io/)
