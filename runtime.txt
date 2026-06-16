from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN missing")

teachers = set()
students = set()

keyboard = ReplyKeyboardMarkup(
    [["🚻", "🍔"], ["💧", "🆘"]],
    resize_keyboard=True
)

message_map = {
    "🚻": "الطالب يريد الذهاب للحمام",
    "🍔": "الطالب جائع",
    "💧": "الطالب يريد ماء",
    "🆘": "الطالب يحتاج مساعدة"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    students.add(uid)
    teachers.discard(uid)
    await update.message.reply_text("اختر الحالة:", reply_markup=keyboard)

async def teacher(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    teachers.add(uid)
    students.discard(uid)
    await update.message.reply_text("تم تسجيلك كمدرس")

async def student(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    students.add(uid)
    teachers.discard(uid)
    await update.message.reply_text("تم تحويلك إلى طالب")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_chat.id

    if text in message_map:
        if uid in teachers:
            await update.message.reply_text("أنت مدرس")
            return

        for t in teachers:
            await context.bot.send_message(t, message_map[text])

        await update.message.reply_text("تم الإرسال")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teacher", teacher))
    app.add_handler(CommandHandler("student", student))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")
    app.run_polling()

if __name__ == "__main__":
    main()