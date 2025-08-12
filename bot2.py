import os
import json
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from telegram.constants import ChatMemberStatus

# Настройки
TOKEN = "8235892772:AAEUSJHCF_eUBkJtS3gUdRHbRQIf6W7HfiU"
DB_FILE = 'members_db.json'

# Инициализация БД
def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                data = f.read()
                if not data.strip():  # Если файл пустой
                    return {}
                return {int(k): set(v) for k, v in json.loads(data).items()}
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump({str(k): list(v) for k, v in data.items()}, f, indent=2)

group_members = load_db()

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Вы сказали: {update.message.text}")

async def list_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
    Доступные команды:
    /list_commands - Список команд
    /members - Показать участников
    /update_members - Обновить список
    """
    await update.message.reply_text(help_text)

async def update_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.chat:
        return

    chat_id = update.message.chat.id
    if chat_id > 0:
        await update.message.reply_text("Команда только для групп!")
        return

    try:
        current_members = set()
        async for member in context.bot.get_chat_members(chat_id):
            if member.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                current_members.add(member.user.id)

        old_members = group_members.get(chat_id, set())
        group_members[chat_id] = current_members
        save_db(group_members)

        report = f"✅ Участников: {len(current_members)}"
        if added := current_members - old_members:
            report += f"\n➕ Новые: {len(added)}"
        if removed := old_members - current_members:
            report += f"\n➖ Ушли: {len(removed)}"
        
        await update.message.reply_text(report)
    except Exception as e:
        print(f"Ошибка: {e}")  # Логируем в консоль
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Ошибка обновления: {str(e)}"
        )

async def show_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in group_members:
        await update.message.reply_text("Сначала используйте /update_members")
        return

    members_list = []
    for user_id in list(group_members[chat_id])[:100]:  # Ограничиваем вывод
        try:
            user = await context.bot.get_chat_member(chat_id, user_id)
            name = user.user.full_name
            members_list.append(f"👤 {name}")
        except:
            members_list.append(f"👤 ID:{user_id}")

    await update.message.reply_text(
        f"Участники ({len(members_list)}):\n" + "\n".join(members_list)
    )

def main():
 # Создаем Application с правильными параметрами (без лишних обратных слешей)
    application = (
        Application.builder()
        .token(TOKEN)
        .http_version("1.1")  # Явно указываем версию HTTP
        .get_updates_http_version("1.1")
        .build()
    )
    # Обработчики
    handlers = [
        CommandHandler("list_commands", list_commands),
        CommandHandler("members", show_members),
        CommandHandler("update_members", update_members),
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    ]
    
    for handler in handlers:
        application.add_handler(handler)
    
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == '__main__':
    # Создаем файл если его нет
    if not os.path.exists(DB_FILE):
        save_db({})
    main()
