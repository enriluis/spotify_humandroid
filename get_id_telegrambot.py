from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler
import asyncio
# Replace 'YOUR_API_TOKEN' with your actual API token
TOKEN = '6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw'

import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola Bienvenid a travez de este bot de telegram recibiras las estadisticas en forma de imagen!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def get_id_chat(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"El ID de chat es: {chat_id} Reenvíe este ID a nuestro contacto y asi podremos enviarle las estadisticas en forma de captura")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    start_handler_get_id_chat = CommandHandler('getchatid', get_id_chat)
    application.add_handler(start_handler_get_id_chat)

    application.run_polling(poll_interval=3)

