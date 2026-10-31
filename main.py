import os
import requests
import time
import schedule
import google.generativeai as genai
from datetime import datetime, timedelta

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_ADS_API_KEY = os.getenv("TELEGRAM_ADS_API_KEY") 
CRICKET_API_KEY = os.getenv("CRICKET_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")
MY_CHAT_ID = "6588318139" 

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def get_upcoming_matches():
    print("Fetching upcoming cricket matches from CricAPI...")
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={CRICKET_API_KEY}&offset=0"
    try:
        response = requests.get(url).json()
        if response.get("status") != "success": 
            return []
        
        upcoming = []
        for match in response.get("data", []):
            match_date_str = match.get("date")
            if match_date_str:
                match_date = datetime.strptime(match_date_str, "%Y-%m-%d")
                if datetime.now() <= match_date <= datetime.now() + timedelta(days=3):
                    upcoming.append(f"{match['name']} on {match_date_str}")
        return upcoming
    except Exception as e:
        print(f"Match fetch fail hua: {e}")
        return []

def gemini_brain_analysis(match_data, performance_data):
    print(f"Running AI analysis using model: {MODEL_NAME}")
    prompt = f"""
    Tum ek expert Telegram Ads media buyer ho. 
    Aaj ke ads ka performance yeh hai: {performance_data}
    Aane wale cricket matches yeh hain: {match_data}
    
    Tasks:
    1. Performance data analyze karo. Agar kisi channel ki Cost Per Join (CPA) target se kam aur sasti hai, toh uska CPM thoda badhane ka logic do. Agar joins nahi aa rahe, to CPM girane ya pause karne ka kaho.
    2. Upcoming cricket match ke hisab se ek highly engaging, urgency-driven (Hinglish) short Ad Copy likho jo mere targeted channel ke liye ho.
    3. Mujhe ek short, point-to-point daily report do jo main apne operations ke liye use kar saku.
    """
    try:
        time.sleep(2) 
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"🚨 AI Analysis Error: {e}"

def send_telegram_report(report_text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": MY_CHAT_ID,
        "text": f"🤖 AI Manager Report (Model: {MODEL_NAME}) 🤖\n\n{report_text}",
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
        print("Report successfully sent to Telegram.")
    except Exception as e:
        print(f"Telegram message fail hua: {e}")

def run_ai_ads_manager():
    print("Running AI Ads Manager cycle...")
    current_performance = "Channel X: 120 Joins (₹4/join). Channel Y: 15 Joins (₹12/join). Target is ₹8/join."
    matches = get_upcoming_matches()
    match_context = ", ".join(matches) if matches else "Agli 3 din me koi bada match nahi hai."
    ai_decision = gemini_brain_analysis(match_context, current_performance)
    send_telegram_report(ai_decision)
    print("Cycle Complete. Waiting for next schedule.")

if name == "__main__":
    print(f"System Booting Up... AI Manager Active on {MODEL_NAME}!")
    run_ai_ads_manager()
    schedule.every(6).hours.do(run_ai_ads_manager)
    while True:
        schedule.run_pending()
        time.sleep(60)
