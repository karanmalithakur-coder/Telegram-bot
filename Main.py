import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Logging chalu karte hain taaki error saaf-saaf dikhe
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")
TELEGRAM_ADS_API_KEY = os.getenv("TELEGRAM_ADS_API_KEY")

if AI_API_KEY:
    genai.configure(api_key=AI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("Warning: AI_API_KEY not found!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    try:
        prompt = f"Aap ek expert Telegram Ads Manager hain. User ka command ye hai: '{user_text}'. Iska professional jawab dein."
        response = model.generate_content(prompt)
        reply_text = response.text
    except Exception as e:
        reply_text = f"Maaf kijiye, AI response generate karne mein error aaya: {str(e)}"

    await context.bot.send_message(chat_id=chat_id, text=reply_text)

if name == '__main__':
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing!")
    else:
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("Bot is running smoothly...")
        app.run_polling()
