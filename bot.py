import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Настройки
TOKEN = "8235892772:AAEUSJHCF_eUBkJtS3gUdRHbRQIf6W7HfiU"  # ← Замените здесь!
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Привет! Я твой первый бот 🤖\nОтправь /help для помощи!')

# Команда /help
def help(update: Update, context: CallbackContext):
    update.message.reply_text('Просто напиши что-нибудь, и я повторю!')

# Ответ на сообщения
def echo(update: Update, context: CallbackContext):
    update.message.reply_text(f"Ты сказал: {update.message.text}")

# Запуск
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
