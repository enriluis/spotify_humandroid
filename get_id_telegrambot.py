from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
# Replace 'YOUR_API_TOKEN' with your actual API token
TOKEN = '6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw'
def start(update: Update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(f"Your chat ID is: {chat_id}")
def main():
    bot = Bot(token=TOKEN)
    updater = Updater(bot=bot, use_context=True)
    # Register the '/start' command handler
    updater.dispatcher.add_handler(CommandHandler('start', start))
    # Start the bot
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()