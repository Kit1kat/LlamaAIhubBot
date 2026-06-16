import os

# Telegram токен
TG_TOKEN = os.getenv("TG_TOKEN")

# Fireworks API ключ
FIREWORKS_KEY = os.getenv("FIREWORKS_KEY")

# Модель Llama для использования
MODEL_NAME = "accounts/fireworks/models/llama-v3-8b-instruct"

# Файл для сохранения памяти
MEMORY_FILE = "memory.json"

# Максимальное количество сообщений в памяти
MAX_MEMORY_MESSAGES = 20