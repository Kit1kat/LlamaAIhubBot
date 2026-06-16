import json
import os
from config import MEMORY_FILE, MAX_MEMORY_MESSAGES

def load_memory():
    """Загружает память из файла"""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка при загрузке памяти: {e}")
    return []

def save_memory(memory):
    """Сохраняет память в файл"""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении памяти: {e}")

def add_to_memory(message):
    """Добавляет сообщение в память"""
    memory = load_memory()
    memory.append(message)
    
    # Удаляем старые сообщения если превышен лимит
    if len(memory) > MAX_MEMORY_MESSAGES:
        memory = memory[-MAX_MEMORY_MESSAGES:]
    
    save_memory(memory)

def clear_memory():
    """Очищает память"""
    save_memory([])

def get_memory_text():
    """Получает память в виде текста"""
    memory = load_memory()
    if not memory:
        return "🧠 Память пуста"
    return "🧠 Память:\n" + "\n".join([f"• {msg}" for msg in memory])