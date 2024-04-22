import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes,InlineQueryHandler
from playlist_info import obtener_info_playlist_from_spotify
from function_utils_aux import obtener_hora_actual,read_config
your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, spotify_client_id, spotify_client_secret = read_config()


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola Bienvenido a travéz de este bot de telegram recibiras las estadísticas en forma de captura!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def get_id_chat(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=f"El ID del chat es: {chat_id} Reenvíe este ID a nuestro contacto y asi podremos enviarle las estadisticas en forma de captura")

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot_token).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    
    application.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    start_handler_get_id_chat = CommandHandler('getchatid', get_id_chat)
    application.add_handler(start_handler_get_id_chat)

    application.run_polling(poll_interval=5)

