# scripts/chat_history.py

import os
import json
from datetime import datetime

# 📁 Directory to store logs
LOG_DIR = "chat_logs"
os.makedirs(LOG_DIR, exist_ok=True)

# 📘 Optional: master session file
SESSION_FILE = os.path.join(LOG_DIR, "session_history.json")

def save_interaction(question, answer):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_data = {
        "timestamp": timestamp,
        "question": question,
        "answer": answer
    }

    # Save to individual timestamped file
    file_name = f"log_{timestamp.replace(':', '-').replace(' ', '_')}.json"
    file_path = os.path.join(LOG_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)

    # Append to session-wide history
    try:
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        else:
            history = []

        history.append(log_data)

        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)

    except Exception as e:
        print(f"⚠️ Could not update session history: {e}")

# ── History-reader helpers ────────────────────────────────────────────────────
import glob
from typing import List, Dict

def list_log_files() -> List[str]:
    """Return log files sorted newest-first."""
    files = glob.glob(os.path.join(LOG_DIR, "log_*.json"))
    return sorted(files, reverse=True)

def load_log(filepath: str) -> Dict:
    """Load a single log JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def clear_logs():
    for filename in os.listdir(LOG_DIR):
        if filename.endswith(".json"):
            os.remove(os.path.join(LOG_DIR, filename))
