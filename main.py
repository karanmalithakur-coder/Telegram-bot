join(matches) if matches else "Agli 3 din me koi bada match nahi hai."
    
    # 2. Gemini se analysis aur Ad Copy banwao
    ai_decision = gemini_brain_analysis(match_context, current_performance)
    
    # 3. Report Telegram par bhej do
    send_telegram_report(ai_decision)
    print("Cycle Complete. Waiting for next schedule.")

# ==========================================
# 4. SCHEDULER (24/7 Run Karne Ke Liye)
# ==========================================
if name == "__main__":
    print(f"System Booting Up... AI Manager Active on {MODEL_NAME}!")
    
    # Deploy hote hi pehli baar turant run karega
    run_ai_ads_manager()
    
    # Phir har 6 ghante mein background me chalega (Din me 4 baar)
    schedule.every(6).hours.do(run_ai_ads_manager)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
