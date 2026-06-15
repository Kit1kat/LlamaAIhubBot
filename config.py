import os

TG_TOKEN = os.getenv("TG_TOKEN")
FIREWORKS_KEY = os.getenv("FIREWORKS_KEY")

MODEL_NAME = "accounts/fireworks/models/llama-v3-8b-instruct"

MEMORY_FILE = "memory.json"
MAX_MEMORY_MESSAGES = 20
