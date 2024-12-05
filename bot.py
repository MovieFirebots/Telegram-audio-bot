import os
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,  # Use DEBUG for detailed logs
)
logger = logging.getLogger(__name__)

# Initialize Flask app
server = Flask(__name__)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received /start from {update.effective_user.username}")
    await update.message.reply_text("Send me a file's download link!")

# Message handler for processing file links
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received link: {update.message.text}")
    # TODO: Add logic to process file and send back
    await update.message.reply_text("Processing your file...")

# Telegram bot runner
async def run_bot():
    # Get bot token from environment variables
    bot_token = os.getenv("YOUR_API_TOKEN")
    if not bot_token:
        logger.error("Bot token is missing. Set it in environment variables.")
        return

    # Create Telegram bot application
    app = Application.builder().token(bot_token).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    logger.info("Starting Telegram bot polling...")
    await app.run_polling(close_loop=False)

# Flask route (required for Render to detect a live service)
@server.route("/")
def home():
    return "Telegram bot is running!"

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Run Telegram bot and Flask concurrently
    loop.create_task(run_bot())
    
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting Flask server on port {port}...")
    server.run(host="0.0.0.0", port=port)
