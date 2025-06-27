# app.py

import os
import streamlit as st
from scripts.chat_engine import generate_answer
from scripts.chat_history import save_interaction, list_log_files, load_log, clear_logs
import pyperclip

# ─── Simple Auth ──────────────────────────────────────────────────────────────
USERNAME = "admin"
PASSWORD = "1234"

def login():
    st.title("🔒 Login Required")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == USERNAME and pwd == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

# ─── Login Check ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

# ─── Main App ─────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Private AI Document Assistant", layout="wide")
st.title("📚 Private AI Document Assistant")
st.markdown("Ask anything from your internal PDFs — runs fully offline.")

# ── Sidebar: Logo, Chat History ───────────────────────────────────────────────
with st.sidebar:
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)
    else:
        st.markdown("### 🧠 Private AI Assistant")

    st.markdown("_Query your company docs privately._")
    st.markdown("---")

    st.subheader("🕑 Chat History")
    history_files = list_log_files()

    if history_files:
        selected = st.selectbox(
            "Select a past question:",
            history_files,
            format_func=lambda p: os.path.basename(p).replace("log_", "").replace(".json", "")
        )
        if selected:
            log = load_log(selected)
            st.write(f"**Q:** {log['question']}")
            st.write(f"**A:** {log['answer']}")
    else:
        st.caption("No chat logs yet.")

    if st.button("🧹 Clear History"):
        clear_logs()
        st.success("Chat history cleared!")

    st.markdown("---")
    st.caption("Built with llama.cpp + ChromaDB + Streamlit")

# ── Main Chat Interface ────────────────────────────────────────────────────────
question = st.text_input("💬 Enter your question:")

if question:
    with st.spinner("Thinking..."):
        raw_answer = generate_answer(question)
        answer = raw_answer.replace("\n", " ").replace("  ", " ").strip()

        st.markdown("---")
        st.markdown(f"**Answer:** {answer}")

        if st.button("📋 Copy"):
            pyperclip.copy(answer)
            st.success("Answer copied to clipboard!")

        save_interaction(question, answer)
        st.markdown("---")
