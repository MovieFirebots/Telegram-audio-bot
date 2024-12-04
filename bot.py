import os
import subprocess
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Path for saving files temporarily
DOWNLOAD_PATH = "./downloads"
os.makedirs(DOWNLOAD_PATH, exist_ok=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Send me a file's download link, and I'll remove the audio and return the modified file!")

def handle_link(update: Update, context: CallbackContext):
    url = update.message.text
    update.message.reply_text("Downloading the file...")

    try:
        # Download the file
        file_name = os.path.join(DOWNLOAD_PATH, "input_file.mp4")
        output_file = os.path.join(DOWNLOAD_PATH, "output_file.mp4")
        subprocess.run(["wget", "-O", file_name, url], check=True)

        # Process the file with FFmpeg to remove audio
        update.message.reply_text("Removing audio...")
        subprocess.run(["ffmpeg", "-i", file_name, "-an", output_file], check=True)

        # Send the processed file back
        update.message.reply_document(document=open(output_file, "rb"))
        update.message.reply_text("Here is your file without audio!")

    except Exception as e:
        update.message.reply_text(f"An error occurred: {e}")

def main():
    # Replace 'YOUR_API_TOKEN' with your bot's token
    updater = Updater("YOUR_API_TOKEN", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
