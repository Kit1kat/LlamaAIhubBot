from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai import llama_answer
from memory import add_to_memory, load_memory

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💬 Новый диалог", callback_data="new_dialog")],
        [InlineKeyboardButton("🧠 Память", callback_data="memory")],
        [InlineKeyboardButton("❌ Сбросить память", callback_data="reset_memory")]
    ]

    await update.message.reply_text(
        "👋 Привет! Я — LlamaAIhubBot 🦙\nРаботаю на Fireworks AI (Llama 3).\nВыбери действие ниже:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "new_dialog":
        context.user_data["history"] = []
        await query.edit_message_text("💬 Новый диалог начат.")

    elif query.data == "memory":
        mem = load_memory()
        text = "🧠 Память пуста." if not mem else "\n".join(mem)
        await query.edit_message_text(f"🧠 Память:\n{text}")

    elif query.data == "reset_memory":
        context.user_data["history"] = []
        await query.edit_message_text("🧹 Память очищена.")

# Сообщения
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # сохраняем в историю
    history = context.user_data.get("history", [])
    history.append({"role": "user", "content": user_text})
    context.user_data["history"] = history

    # отправляем в Fireworks
    answer = await llama_answer(history)

    # сохраняем ответ
    history.append({"role": "assistant", "content": answer})
    context.user_data["history"] = history

    # отправляем пользователю
    await update.message.reply_text(answer)
