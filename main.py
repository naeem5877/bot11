import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def create_bot():
    # Set your bot token here
    TOKEN = 'YOUR_BOT_TOKEN'

    # Set the path where files will be stored
    FILE_STORAGE_PATH = 'files/'

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # Create the Updater and pass it your bot's token
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Define the start command handler
    def start(update: Update, context: CallbackContext) -> None:
        update.message.reply_text('Hello! I am your file storage bot. Send me any file, and I will save it for you.')

    # Define the file handler
    def handle_file(update: Update, context: CallbackContext) -> None:
        file_id = update.message.document.file_id
        file = context.bot.get_file(file_id)
        file_path = os.path.join(FILE_STORAGE_PATH, file_id + '_' + update.message.document.file_name)
        file.download(file_path)

        update.message.reply_text(f'File {update.message.document.file_name} has been saved. Use /search to find it.')

    # Define the search command handler
    def search(update: Update, context: CallbackContext) -> None:
        query = ' '.join(context.args)
        files = [f for f in os.listdir(FILE_STORAGE_PATH) if query.lower() in f.lower()]

        if files:
            file_list = '\n'.join(files)
            update.message.reply_text(f'Files matching your search:\n{file_list}')
        else:
            update.message.reply_text('No files found.')

    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("search", search, pass_args=True))

    # Register message handler for files
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    return updater
