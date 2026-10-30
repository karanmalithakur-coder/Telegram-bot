import os
import logging
import time
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Flask Web Server
app_web = Flask('')

@app_web.route('/')
def home():
    return "Telegram AI Bot is live and running!"

def run_bot():
    time.sleep(2)
    
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    ai_key = os.getenv("AI_API_KEY")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is missing!")
        return

    if ai_key:
        genai.configure(api_key=ai_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        logger.error("AI_API_KEY is missing!")
        return

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

    try:
        logger.info("Starting Telegram Bot application...")
        app = ApplicationBuilder().token(token).build()
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")

# Bina kisi 'if name' check ke seedha run karte hain taaki error ka scope hi na rahe!
bot_thread = Thread(target=run_bot, daemon=True)
bot_thread.start()

port = int(os.environ.get("PORT", 8080))
logger.info(f"Starting Flask web server on port {port}...")
app_web.run(host='0.0.0.0', port=port, use_reloader=False)
