elif action_data.get("action_type") == "add_campaign":
                        camp_data = action_data["data"]
                        if camp_data:
                            camp_data["executed"] = False
                            current_memory["campaigns"].append(camp_data)
                            save_memory(current_memory)
                            ai_reply += "\n\n✅ *[System Log]: New Campaign successfully scheduled and saved to Python Persistent Memory!*"
                except Exception as parse_err:
                    logger.error(f"Memory Parse Error: {parse_err}")
            
            reply_text = ai_reply
        except Exception as e:
            logger.error(f"AI Error: {e}")
            reply_text = f"Technical Error: {str(e)}"
            
        await context.bot.send_message(chat_id=chat_id, text=reply_text, parse_mode="Markdown")

    # Start Background Scheduler Thread
    admin_id = os.getenv("ADMIN_CHAT_ID", "0000000")
    scheduler_thread = Thread(target=background_scheduler_worker, args=(token, admin_id), daemon=True)
    scheduler_thread.start()

    try:
        logger.info("Starting Telegram Bot Polling with Memory Bridge...")
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.run_polling(drop_pending_updates=True, stop_signals=None)
    except Exception as e:
        logger.error(f"Telegram bot error: {e}")

# Run Bot in background thread so Flask runs concurrently on Render
bot_thread = Thread(target=run_bot, daemon=True)
bot_thread.start()

port = int(os.environ.get("PORT", 8080))
logger.info(f"Starting Flask web server on port {port}...")
app_web.run(host='0.0.0.0', port=port, use_reloader=False)
