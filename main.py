import os
import time
import json
import logging
from threading import Thread
from datetime import datetime
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

DB_FILE = "bot_memory.json"

def load_memory():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_link": "https://t.me/+DefaultBackupChannelLink",
        "campaigns": []
    }

def save_memory(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

app_web = Flask('')

@app_web.route('/')
def home():
    return "🔥 Telegram Bot is LIVE!"

def background_scheduler_worker(bot_token, admin_chat_id):
    import requests
    base_url = f"https://api.telegram.org/bot{bot_token}"
    while True:
        try:
            memory = load_memory()
            now = datetime.now()
            for camp in memory.get("campaigns", []):
                if not camp.get("executed", False):
                    target_time = datetime.strptime(camp["schedule_time"], "%Y-%m-%d %H:%M:%S")
                    if now >= target_time:
                        link = memory.get("active_link", "https://t.me/DefaultLink")
                        msg = f"🚨 *CAMPAIGN ALERT* 🚨\n\n{camp['match_name']}\n{camp['ad_copy']}\n\n[Join Here]({link})"
                        requests.post(f"{base_url}/sendMessage", json={"chat_id": admin_chat_id, "text": msg, "parse_mode": "Markdown"})
                        camp["executed"] = True
                        save_memory(memory)
        except Exception as e:
            logger.error(f"Error: {e}")
        time.sleep(30)

def run_bot():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    ai_key = os.getenv("AI_API_KEY")
    if not token or not ai_key:
        return
    genai.configure(api_key=ai_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 Bot is active and ready!", parse_mode="Markdown")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        chat_id = update.message.chat_id
        current_memory = load_memory()
        prompt = f"You are a telegram marketing expert. Memory: {json.dumps(current_memory)}. User said: {user_text}"
        res = model.generate_content(prompt)
        await context.bot.send_message(chat_id=chat_id, text=res.text, parse_mode="Markdown")

    admin_id = os.getenv("ADMIN_CHAT_ID", "0000000")
    Thread(target=background_scheduler_worker, args=(token, admin_id), daemon=True).start()

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling(drop_pending_updates=True)

Thread(target=run_bot, daemon=True).start()

if name == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)
