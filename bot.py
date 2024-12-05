import os
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Code
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file's download link!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Processing your request...")

async def run_bot():
    app = Application.builder().token(os.getenv("YOUR_API_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    # Start polling
    await app.run_polling()

# Flask Server for Render
server = Flask(__name__)

@server.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    # Run Flask and Telegram bot concurrently
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())
    
    # Get the port from the environment (Render sets it)
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port) 

import logging

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Add a log message in the start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start from {update.effective_user.username}")
    await update.message.reply_text("Send me a file's download link!")
