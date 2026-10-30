Punter Psychology & Low CPA: Focus heavily on loss recovery, 90% accuracy trust, toss pass, and session profit hooks to maximize joins at the lowest possible cost.
            
            User's Instruction / Data: '{user_text}'
            
            Deliver a flawless, highly structured, professional, and execution-ready campaign blueprint in Hinglish/English mix. Be ruthless about ROI, low CPA, and maximum conversions.
            """
            
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            response = model.generate_content(master_prompt, safety_settings=safety_settings)
            
            if response.text:
                reply_text = response.text
            else:
                reply_text = "Maaf kijiye, is instruction par response generate nahi ho paya. Dobara try kijiye!"
        except Exception as e:
            logger.error(f"AI Error: {e}")
            reply_text = f"Maaf kijiye, technical error aaya: {str(e)}"
            
        await context.bot.send_message(chat_id=chat_id, text=reply_text)

    try:
        logger.info("Starting Telegram Bot application...")
        app = ApplicationBuilder().token(token).build()
        
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        app.run_polling(drop_pending_updates=True, stop_signals=None)
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")

bot_thread = Thread(target=run_bot, daemon=True)
bot_thread.start()

port = int(os.environ.get("PORT", 8080))
logger.info(f"Starting Flask web server on port {port}...")
app_web.run(host='0.0.0.0', port=port, use_reloader=False)
