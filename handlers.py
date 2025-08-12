from telegram.ext import CommandHandler
from commands import list_commands

def setup_handlers(application):
    application.add_handler(CommandHandler("list_commands", list_commands))
    # Здесь будут добавляться другие обработчики
