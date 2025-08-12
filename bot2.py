from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.constants import ChatMemberStatus
from typing import Dict, Set

TOKEN = "8235892772:AAEUSJHCF_eUBkJtS3gUdRHbRQIf6W7HfiU"

# Глобальное хранилище участников (chat_id -> set_of_user_ids)
group_members: Dict[int, Set[int]] = {}

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")
    
async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Доступные команды:
    /list_commands - Список команд
    /test - пустая тестовая
    /members - Показать участников группы
    /update_members - Обновить список участников
    """
    await update.message.reply_text(help_text)

async def update_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id > 0:
        await update.message.reply_text("Эта команда работает только в группах!")
        return

    try:
        current_members = set()
        # Новый способ получения участников
        async with context.bot as bot:
            async for member in bot.get_chat_members(chat_id):
                if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    current_members.add(member.user.id)

        old_members = group_members.get(chat_id, set())
        group_members[chat_id] = current_members
        save_db(group_members)

        report = f"✅ Список обновлен\n👥 Участников: {len(current_members)}"
        if added := current_members - old_members:
            report += f"\n➕ Новые: {len(added)}"
        if removed := old_members - current_members:
            report += f"\n➖ Ушли: {len(removed)}"
        
        await update.message.reply_text(report)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")
        
async def show_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in group_members or not group_members[chat_id]:
        await update.message.reply_text("Список участников пуст. Используйте /update_members")
        return

    try:
        members_list = []
        for user_id in group_members[chat_id]:
            user = await context.bot.get_chat_member(chat_id, user_id)
            members_list.append(f"👤 {user.user.full_name} (@{user.user.username or 'нет'})")

        await update.message.reply_text(
            f"Участники группы ({len(members_list)}):\n" + "\n".join(members_list)
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(CommandHandler("list_commands", list_commands))
    application.add_handler(CommandHandler("members", show_members))
    application.add_handler(CommandHandler("update_members", update_members))
    
    application.run_polling()

if __name__ == '__main__':
    main()
