from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import asyncio

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN missing")

teachers = set()
students = set()

main_keyboard = ReplyKeyboardMarkup(
    [["🛠️ خدمات"], ["🐾 نشاط الحيوانات"]],
    resize_keyboard=True
)

services_keyboard = ReplyKeyboardMarkup(
    [["🚻", "🍔"], ["💧", "🆘"], ["🔙 رجوع"]],
    resize_keyboard=True
)

animals_keyboard = ReplyKeyboardMarkup(
    [["🌲 الغابة"], ["🏜️ الصحراء"], ["🌊 البحر"], ["🔙 رجوع"]],
    resize_keyboard=True
)

message_map = {
    "🚻": "الطالب يريد الذهاب للحمام",
    "🍔": "الطالب جائع",
    "💧": "الطالب يريد ماء",
    "🆘": "الطالب يحتاج مساعدة"
}

animal_map = {
    "🌲 الغابة": "الطالب اختار نشاط الغابة",
    "🏜️ الصحراء": "الطالب اختار نشاط الصحراء",
    "🌊 البحر": "الطالب اختار نشاط البحر"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_chat.id
    students.add(uid)
    teachers.discard(uid)

    await update.message.reply_text("اختر:", reply_markup=main_keyboard)


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

    if text == "🛠️ خدمات":
        await update.message.reply_text("اختر خدمة:", reply_markup=services_keyboard)
        return

    if text == "🐾 نشاط الحيوانات":
        await update.message.reply_text("اختر بيئة:", reply_markup=animals_keyboard)
        return

    if text == "🔙 رجوع":
        await update.message.reply_text("القائمة:", reply_markup=main_keyboard)
        return

    # خدمات
    if text in message_map:
        if uid in teachers:
            await update.message.reply_text("أنت مدرس")
            return

        for t in teachers:
            await context.bot.send_message(chat_id=t, text=message_map[text])

        await update.message.reply_text("تم الإرسال")
        return

    # الحيوانات (هنا التعديل المهم)
    if text in animal_map:
        if uid in teachers:
            await update.message.reply_text("أنت مدرس")
            return

        for t in teachers:
            await context.bot.send_message(chat_id=t, text=animal_map[text])

        await update.message.reply_text("تم الإرسال")
        return


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("teacher", teacher))
    app.add_handler(CommandHandler("student", student))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("BOT RUNNING")

    # مهم جداً للـ Render / Railway
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
