from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai
import os
from io import BytesIO
from PIL import Image

# مفاتيح من السيرفر (Render)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# نص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )
    await update.message.reply_text(response.choices[0].message.content)

# صورة
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("وصلتني الصورة ✅")

# صوت
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = await update.message.voice.get_file()
    await voice.download_to_drive("voice.ogg")
    audio = open("voice.ogg", "rb")
    transcript = openai.Audio.transcriptions.create(
        model="whisper-1",
        file=audio
    )
    await update.message.reply_text("قلت: " + transcript["text"])

# تشغيل البوت
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

app.run_polling()
