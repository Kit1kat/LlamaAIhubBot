from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai import llama_answer
from memory import add_to_memory, load_memory, clear_memory, get_memory_text

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = [
        [InlineKeyboardButton("💬 Новый диалог", callback_data="new_dialog")],
        [InlineKeyboardButton("🧠 Память", callback_data="memory")],
        [InlineKeyboardButton("❌ Сбросить память", callback_data="reset_memory")]
    ]

    await update.message.reply_text(
        "👋 Привет! Я — LlamaAIhubBot 🦙\nРаботаю с памятью и AI!\n\n"
        "Просто пиши мне сообщения, и я буду отвечать на основе Llama AI 🤖",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Обработчик кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик inline кнопок"""
    query = update.callback_query
    await query.answer()

    if query.data == "new_dialog":
        context.user_data["history"] = []
        await query.edit_message_text("💬 Новый диалог начат. Можешь писать сообщения!")

    elif query.data == "memory":
        mem_text = get_memory_text()
        await query.edit_message_text(mem_text)

    elif query.data == "reset_memory":
        clear_memory()
        context.user_data["history"] = []
        await query.edit_message_text("🧹 Память очищена.")

# Обработчик сообщений
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик входящих сообщений от пользователя"""
    user_text = update.message.text
    
    # Показываем что бот печатает
    await update.message.chat.send_action("typing")

    # Сохраняем в историю
    history = context.user_data.get("history", [])
    history.append({"role": "user", "content": user_text})
    context.user_data["history"] = history

    # Отправляем в Fireworks API и получаем ответ
    answer = await llama_answer(history)

    # Сохраняем ответ в историю
    history.append({"role": "assistant", "content": answer})
    context.user_data["history"] = history

    # Отправляем пользователю
    await update.message.reply_text(answer)