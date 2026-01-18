from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI
import os

# قراءة المفاتيح من Render Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# تهيئة عميل OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# دالة التعامل مع النصوص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

# دالة التعامل مع الصور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("وصلتني الصورة ✅")

# دالة التعامل مع الصوت
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await update.message.voice.get_file()
    await voice_file.download_to_drive("voice.ogg")
    with open("voice.ogg", "rb") as audio:
        transcript = client.audio.transcriptions.create(
            file=audio,
            model="whisper-1"
        )
    await update.message.reply_text("قلت: " + transcript.text)

# تشغيل البوت
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

app.run_polling()