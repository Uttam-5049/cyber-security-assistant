import os
import json
import datetime
import streamlit as st

METRIC_LOG_FILE = os.path.join("metrics_logs", "feedback_log.json")  # Absolute path for debugging

def log_feedback(question, answer, is_correct):
    try:
        feedback_entry = {
            "question": question,
            "answer": answer,
            "correct": is_correct,
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Ensure directory exists
        os.makedirs(os.path.dirname(METRIC_LOG_FILE), exist_ok=True)
        # Load existing logs
        logs = []
        if os.path.exists(METRIC_LOG_FILE):
            with open(METRIC_LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)

        logs.append(feedback_entry)

        with open(METRIC_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2)

        # Also log in test_log.txt
        with open("metrics_logs/test_log.txt", "a", encoding="utf-8") as f:
            status = "✅ Correct" if is_correct else "❌ Incorrect"
            f.write(f"[{feedback_entry['timestamp']}] FEEDBACK - {status}\n")
            f.write(f"Q: {question}\nA: {answer[:200]}...\n\n")

        # DEBUG
        print("[FEEDBACK LOGGER] Feedback logged successfully.")
        st.info("[FEEDBACK LOGGER] Feedback logged successfully.")  # Show in UI

    except Exception as e:
        print(f"[FEEDBACK LOGGER ERROR] {e}")
        st.error(f"[FEEDBACK LOGGER ERROR] {e}")


def load_feedback_stats():
    if not os.path.exists(METRIC_LOG_FILE):
        return 0, 0
    correct, incorrect = 0, 0
    with open(METRIC_LOG_FILE, "r", encoding="utf-8") as f:
        try:
            entries = json.load(f)
            for entry in entries:
                if entry.get("correct") is True:
                    correct += 1
                elif entry.get("correct") is False:
                    incorrect += 1
        except json.JSONDecodeError:
            pass
    return correct, incorrect


def log_engagement_metrics(question_count, session_start_time):
    
    correct, incorrect = load_feedback_stats()

    metrics = {
        "questions_asked": question_count,
        "session_duration_secs": int(datetime.datetime.now().timestamp() - session_start_time),
        "feedback": {
            "correct": correct,
            "incorrect": incorrect
        }
    }

    with open("metrics_logs/engagement_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open("metrics_logs/test_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now().isoformat()}] SESSION METRICS\n")
        f.write(f"Questions asked: {metrics['questions_asked']}\n")
        f.write(f"Session duration: {metrics['session_duration_secs']} seconds\n")
        f.write(f"Correct feedback: {correct}\nIncorrect feedback: {incorrect}\n\n")
