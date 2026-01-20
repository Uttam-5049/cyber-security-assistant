import os

DATA_FOLDER = "data"
VECTOR_DB_PATH = "vector_db"
NVD_API_KEY = os.getenv("NVD_API_KEY", "24602b0b-84ad-4090-bcd4-e51ba67ebd7f")
MODEL_PATH = os.getenv("MODEL_PATH", r"C:\Users\kevin\llama.cpp\models\mistral\mistral-7b-instruct-v0.1.Q3_K_M.gguf")
HISTORY_FILE = "chat_logs/history.json"
METRICS_LOGS = "metrics_logs"
TEST_LOG_FILE = os.path.join(METRICS_LOGS, "test_log.txt")
