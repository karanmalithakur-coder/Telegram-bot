import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# 1. Web Server (Render ke health check ko satisfy karne ke liye)
app_web = Flask('')

@app_web.route('/')
def home():
    return "Telegram AI Bot is live and running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port, use_reloader=False)

# 2. Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 3. Environment Variables se Keys uthana
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
AI_API_KEY = os.getenv("AI_API_KEY")
TELEGRAM_ADS_API_KEY = os.getenv("TELEGRAM_ADS_API_KEY")

if AI_API_KEY:
    genai.configure(api_key=AI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    try:
        prompt = f"Aap ek expert Telegram Ads Manager aur Data Analyst hain. User ka command ye hai: '{user_text}'. Iska professional jawab dein."
        response = model.generate_content(prompt)
        reply_text = response.text
    except Exception as e:
        reply_text = f"Maaf kijiye, error aaya: {str(e)}"

    await context.bot.send_message(chat_id=chat_id, text=reply_text)

if name == '__main__':
    # Web Server ko background thread mein start karte hain
    t = Thread(target=run_web)
    t.start()

    # Telegram Bot ko start karte hain
    if not TELEGRAM_BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing!")
    else:
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        print("Bot is running smoothly...")
        app.run_polling()
