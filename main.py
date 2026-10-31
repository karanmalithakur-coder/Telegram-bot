import os
import requests
import time
import google.generativeai as genai
from datetime import datetime, timedelta

# Environment Variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADS_API_KEY = os.getenv("TELEGRAM_ADS_API_KEY") 
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_upcoming_matches():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICKET_API_KEY}&offset=0"
    try:
        response = requests.get(url).json()
        if response.get("status") != "success": 
            return "Koi live match data nahi mila."
        
        upcoming = []
        for match in response.get("data", []):
            match_date_str = match.get("date")
            if match_date_str:
                match_date = datetime.strptime(match_date_str, "%Y-%m-%d")
                if datetime.now() <= match_date <= datetime.now() + timedelta(days=3):
                    upcoming.append(f"{match['name']} on {match_date_str}")
        return ", ".join(upcoming) if upcoming else "Agli 3 din me koi bada match nahi hai."
    except Exception as e:
        return f"Match fetch error: {e}"

def autonomous_media_buyer_brain(user_input_or_context):
    match_context = get_upcoming_matches()
    prompt = f"""
    Tum ek expert autonomous Telegram Ads media buyer aur D2C growth engine ho. 
    Tumhara kaam hai campaigns ko poori tarah se optimize karna:
    - Performance analyze karke expensive/bure ads ko pause karna aur unke naye high-converting creative angles banana.
    - Cost Per Join (CPA) ke hisab se CPM upar ya niche adjust karne ka exact decision lena.
    - Aane wale cricket matches ({match_context}) ke anusar bidding strategy set karna.
    
    User ka input/command yeh hai: "{user_input_or_context}"
    
    Mujhe ekdum clear, action-oriented aur sharp response do jisme:
    1. Campaign Optimization Decision (Kaunsa ad band hua, kiska CPM change hua).
    2. Naye Optimized Ad Creatives & Copies (Hinglish/Urgency driven).
    3. Live execution status jo direct Telegram chat par bheja ja sake.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 Autonomous AI Error: {e}"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Telegram send fail: {e}")

def run_telegram_polling():
    print("Autonomous AI Media Buyer Bot is live and listening...")
    offset = 0
    while True:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
        try:
            response = requests.get(url).json()
            if response.get("ok"):
                for result in response.get("result", []):
                    offset = result["update_id"] + 1
                    message = result.get("message", {})
                    chat_id = message.get("chat", {}).get("id")
                    text = message.get("text")
                    
                    if chat_id and text:
                        print(f"Command received from {chat_id}: {text}")
                        if text.startswith("/start"):
                            welcome_msg = "🤖 **Autonomous Telegram Ads Growth Engine Active!**\n\nMujhe channel ka link ya performance data do. Main khud analyze karke bure ads band karunga, CPM adjust karunga, aur naye creatives generate karunga."
                            send_telegram_message(chat_id, welcome_msg)
                        else:
                            ai_action_report = autonomous_media_buyer_brain(text)
                            send_telegram_message(chat_id, ai_action_report)
        except Exception as e:

print(f"Polling error: {e}")
            time.sleep(5)
        time.sleep(1)

if name == "__main__":
    print(f"System Booting Up... Autonomous Media Buyer Active on {MODEL_NAME}!")
    run_telegram_polling()
