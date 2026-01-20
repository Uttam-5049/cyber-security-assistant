import os
import json
from langchain.schema import HumanMessage, AIMessage
from config import HISTORY_FILE

def load_chat_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                history = []
                for msg in raw:
                    if msg["type"] == "human":
                        history.append(HumanMessage(content=msg["content"]))
                    elif msg["type"] == "ai":
                        history.append(AIMessage(content=msg["content"]))
                return history
        except Exception:
            pass
    return []

def save_chat_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    serializable_history = []
    for message in history:
        if isinstance(message, HumanMessage):
            serializable_history.append({"type": "human", "content": message.content})
        elif isinstance(message, AIMessage):
            serializable_history.append({"type": "ai", "content": message.content})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(serializable_history, f, indent=2)
