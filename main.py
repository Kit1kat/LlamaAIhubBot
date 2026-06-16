import asyncio
from keep_alive import keep_alive
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TG_TOKEN
from handlers import start, button_handler, on_message

async def run_bot():
    """Запускает Telegram бота"""
    app = ApplicationBuilder().token(TG_TOKEN).build()

    # Добавляем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))

    # Запускаем бота
    await app.run_polling()

if __name__ == "__main__":
    # Запускаем keep_alive для поддержания бота в живом состоянии
    keep_alive()
    
    # Запускаем основной цикл бота
    asyncio.run(run_bot())
