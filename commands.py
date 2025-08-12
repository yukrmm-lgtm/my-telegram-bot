async def list_commands(update, context):
    help_text = """
    Доступные команды:
    /list_commands - Список команд
    /test - пустая тестовая
    """
    await update.message.reply_text(help_text)
