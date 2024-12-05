import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Code
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file's download link!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Processing your request...")

def main():
    app = Application.builder().token(os.getenv("YOUR_API_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    # Start polling in a background thread
    import threading
    threading.Thread(target=app.run_polling, daemon=True).start()

# Dummy Flask Server
server = Flask(__name__)

@server.route("/")
def index():
    return "Bot is running!"

if __name__ == "__main__":
    main()
    # Get the port from the environment (Render sets it)
    port = int(os.environ.get("PORT", 5000))
    server.run(host="0.0.0.0", port=port)
