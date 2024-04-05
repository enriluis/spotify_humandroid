

from telegram.ext import Updater, CommandHandler

def obtener_id_de_chat(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text=f"El ID de chat es: {chat_id}")

# Token de tu bot
TOKEN = "6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw"

# Crear el objeto updater y dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Manejador para el comando /getchatid
dispatcher.add_handler(CommandHandler("getchatid", obtener_id_de_chat))

# Iniciar el bot
updater.start_polling()