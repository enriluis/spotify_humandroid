from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual
from colorama import Fore, Style
from telegram import Bot

async def enviar_archivo_telegram(token, chat_ids, archivo=None, caption=None, mensaje=None, max_retries=3):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    bot = Bot(token=token)
    for chat_id in chat_ids:
        chat_id = chat_id.strip() 
        retries = 0
        while retries < max_retries:
            try:
                if archivo and (archivo.endswith('.jpg') or archivo.endswith('.png')):
                    await bot.send_photo(chat_id=chat_id, photo=open(archivo, 'rb'), caption=caption)
                elif archivo:
                    await bot.send_document(chat_id=chat_id, document=open(archivo, 'rb'), caption=caption)
                    print(f"{mensaje_hora} Error en el envío del archivo a {chat_id}")
                elif mensaje:
                    await bot.send_message(chat_id=chat_id, text=mensaje)
                break  
            except Exception as e:
                print(f"{mensaje_hora} Error en el envío del archivo a {chat_id}: {e}")
                retries += 1
        else:
            print(f"{mensaje_hora} Falló el envío del archivo a {chat_id} después de {max_retries} intentos.")
