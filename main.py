import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Logging Setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Flask Web Server (Render health check ke liye)
app_web = Flask('')

@app_web.route('/')
def home():
    return "Telegram AI Bot is live and running!"

def run_bot():
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

    # Start command handler
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Namaste! Main aapka Telegram AI Ads Manager bot hu. Aap mujhse koi bhi sawal puch sakte hain!")

    # Message handler
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
        
        # Handlers add kar rahe hain
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        # Bot polling start
        app.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")

# Bot thread ko start karte hain
bot_thread = Thread(target=run_bot, daemon=True)
bot_thread.start()

# Flask web server ko main thread par chalate hain
port = int(os.environ.get("PORT", 8080))
logger.info(f"Starting Flask web server on port {port}...")
app_web.run(host='0.0.0.0', port=port, use_reloader=False)
