import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from openai import OpenAI
from io import BytesIO

# مفاتيح من Environment Variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# نصوص
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = client.responses.create(
        model="gpt-4o-mini",
        input=user_text
    )
    await update.message.reply_text(response.output_text)

# صور
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("وصلتني الصورة ✅")

# صوت
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice_file = await update.message.voice.get_file()
    bio = BytesIO()
    await voice_file.download(out=bio)
    bio.seek(0)
    transcript = client.audio.transcriptions.create(
        file=bio,
        model="whisper-1"
    )
    await update.message.reply_text("قلت: " + transcript.text)

# تشغيل البوت
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))

app.run_polling()