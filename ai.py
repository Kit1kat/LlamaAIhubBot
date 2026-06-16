import aiohttp
import json
from config import FIREWORKS_KEY, MODEL_NAME
from memory import add_to_memory, load_memory

async def llama_answer(history):
    """
    Отправляет сообщение в Fireworks API и получает ответ от Llama
    """
    if not FIREWORKS_KEY:
        return "❌ FIREWORKS_KEY не установлен. Установите переменную окружения FIREWORKS_KEY."

    try:
        # Загружаем историю из файла памяти
        memory = load_memory()

        # Подготавливаем контекст с памятью
        system_message = """Ты — полезный AI ассистент Llama. 
Ты помогаешь пользователям с информацией, кодом и вопросами.
Отвечай кратко и понятно на русском языке."""

        # Формируем сообщения для API
        messages = [
            {"role": "system", "content": system_message}
        ]

        # Добавляем память в контекст
        if memory:
            messages.append({
                "role": "system",
                "content": f"📝 Память предыдущих разговоров:\n" + "\n".join(memory[:5])
            })

        # Добавляем историю текущего разговора
        messages.extend(history)

        # Отправляем запрос в Fireworks API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.fireworks.ai/inference/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {FIREWORKS_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": messages,
                    "max_tokens": 512,
                    "temperature": 0.7
                }
            ) as response:
                text = await response.text()
                try:
                    data = json.loads(text)
                except Exception:
                    # если не JSON — вернём текст напрямую
                    return text or "❌ Пустой ответ от API"

                # Пытаемся извлечь текст в нескольких вариантах
                answer = None
                if isinstance(data, dict):
                    if "choices" in data and data["choices"]:
                        ch = data["choices"][0]
                        if isinstance(ch, dict):
                            # OpenAI-like structure
                            answer = ch.get("message", {}).get("content") or ch.get("text")
                    if not answer:
                        answer = data.get("output") or data.get("text") or data.get("result")
                elif isinstance(data, list) and data:
                    first = data[0]
                    if isinstance(first, dict):
                        answer = first.get("text") or first.get("message")

                if not answer:
                    # fallback — вернуть сериализованный объект
                    answer = json.dumps(data, ensure_ascii=False)

                # Сохраняем в память
                if history and len(history) > 0:
                    user_msg = history[-1].get("content", "")[:50]
                    add_to_memory(f"Q: {user_msg}... A: {str(answer)[:50]}...")

                return answer

    except Exception as e:
        return f"❌ Ошибка при обращении к AI: {str(e)}"
