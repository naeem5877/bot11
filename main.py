import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6743376677:AAG-stp9PLS3UI7JPosoIoz_1x8K61_QYTY'
SAVE_PATH = 'files/'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to the Storage Bot! Send me any file, and I will save it for you.')

def save_file(update: Update, context: CallbackContext) -> None:
    file_id = update.message.document.file_id
    file = context.bot.get_file(file_id)
    file.download(os.path.join(SAVE_PATH, file.file_path.split("/")[-1]))
    update.message.reply_text('File saved successfully!')

def search_files(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    file_list = [f for f in os.listdir(SAVE_PATH) if query.lower() in f.lower()]
    if file_list:
        file_list_str = '\n'.join(file_list)
        update.message.reply_text(f"Matching files:\n{file_list_str}")
    else:
        update.message.reply_text("No matching files found.")

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, save_file))
    dp.add_handler(CommandHandler("search", search_files, pass_args=True))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)
    main()
