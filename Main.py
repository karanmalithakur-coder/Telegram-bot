import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Teeno Keys jo apne nikaali hain, wo yahan automatic cloud se uthegi
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")
TELEGRAM_ADS_API_KEY = os.getenv("TELEGRAM_ADS_API_KEY")

genai.configure(api_key=AI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    # Gemini AI ko instructions
    prompt = f"""
    Aap ek expert Telegram Ads Manager aur Data Analyst hain.
    User ka command ye hai: '{user_text}'
    Iske basis par professional ad copy likhein ya performance analysis explain karein.
    """
    
    response = model.generate_content(prompt)
    reply_text = response.text

    # Telegram Bot par wapas message bhejna
    await context.bot.send_message(chat_id=chat_id, text=reply_text)

if name == '__main__':
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing!")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
