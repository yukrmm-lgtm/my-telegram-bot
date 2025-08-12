from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
from telegram.ext import filters

TOKEN = "8235892772:AAEUSJHCF_eUBkJtS3gUdRHbRQIf6W7HfiU"  # Замените на реальный токен

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я твой бот!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

def main():
    # Создаем Application вместо Updater
    application = Application.builder().token(TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
