import os
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Path for saving files temporarily
DOWNLOAD_PATH = "./downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send me a file's download link, and I'll remove the audio and return the modified file!")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Downloading the file...")

    try:
        # Download the file
        file_name = os.path.join(DOWNLOAD_PATH, "input_file.mp4")
        output_file = os.path.join(DOWNLOAD_PATH, "output_file.mp4")
        subprocess.run(["wget", "-O", file_name, url], check=True)

        # Process the file with FFmpeg to remove audio
        await update.message.reply_text("Removing audio...")
        subprocess.run(["ffmpeg", "-i", file_name, "-an", output_file], check=True)

        # Send the processed file back
        await update.message.reply_document(document=open(output_file, "rb"))
        await update.message.reply_text("Here is your file without audio!")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {e}")

def main():
    # Replace 'YOUR_API_TOKEN' with your bot's token
    app = Application.builder().token("YOUR_API_TOKEN").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))

    app.run_polling()

if __name__ == "__main__":
    main()
