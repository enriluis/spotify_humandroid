import calendar,string, random, time, requests, re, os,subprocess,pyautogui, configparser, datetime,sys
from random import randint, choice, choices
from colorama import Fore, Style
from function_utils_aux import buscar_imagen_y_clic,obtener_hora_actual,read_config,close_firefox_window

# Verificar si se pasaron los argumentos enecesarios y si no leerlo desde archivo.
playlist_id = sys.argv[1]
nombre_playlist = str(sys.argv[2])
playlist_duration = str(sys.argv[3])

"""
    if len(sys.argv) == 4:
    # Cargar los argumentos como variables
    playlist_id = sys.argv[1]
    nombre_playlist = str(sys.argv[2])
    playlist_duration = str(sys.argv[3])
else:
    # Cargar las variables desde el archivo
    your_username, your_password, fecha_creacion,playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()
"""
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
## Leer la playlist_id y la descripción
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "account.txt"))

your_username = config['Credentials']['username']
your_password = config['Credentials']['password']
normalized_playlistname = re.sub(r'[^\w\-_.]', '', nombre_playlist)
# Obtener la ruta absoluta del directorio del script
directorio_actual = os.path.dirname(os.path.abspath(__file__))
url_estaditicas_spotify = "https://www.statsforspotify.com/track/recent"
# Comando para abrir Firefox con la URL
firefox_command = f'firefox {url_estaditicas_spotify} &'

pausa = random.uniform(1000, 2000) / 1000
pyautogui.PAUSE = pausa
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
DIRECTORY = os.path.join(os.path.dirname(__file__), "Stats") 
now = datetime.datetime.now()    # Obtener la fecha y hora actual
timestamp = now.strftime("%d-%m-%Y_%H-%M")
#   normalized_filename = re.sub(r'[^\w\-_.]', '', nombre_playlist)
filename = "{}_{}.pdf".format(normalized_playlistname, timestamp)
nombre_archivo = (os.path.join(DIRECTORY, filename))




def iniciar_sesion():
    # Recorre el formulario de creación de la cuenta y rellena los campos de nombre de usuario y contraseña.
    for _ in range(4):
        pyautogui.press('tab', interval=0.2)
    pyautogui.typewrite(your_username, interval=0.2)
    pyautogui.press('tab')
    pyautogui.typewrite(your_password, interval=0.2)
    time.sleep(3.5)
    # Haz clic en el botón "Entrar".
    for _ in range(3):
        pyautogui.press('tab', interval=0.2)
    pyautogui.press('enter')
    time.sleep(5.5)

def permitir_acceso_estadisticas():
    if buscar_imagen_y_clic("allow_spotify_to_connect_stats.png", grayscale=True, confidence=0.8):
        time.sleep(pausa)
        for _ in range(3):
            pyautogui.press('tab', interval=0.2)
        pyautogui.press('enter')
        print(f"{mensaje_hora} Permitir el acceso de la cuenta {your_username} a las estadisticas")
    else:
        print(f"{mensaje_hora} No se encontró la imagen 'allow_spotify_to_connect_stats.png'")

def salvar_pagina_como_pdf():
    if buscar_imagen_y_clic("Recently_played_Tracks.png", grayscale=True, confidence=0.8):
        time.sleep(pausa)
        print(f"{mensaje_hora} Se accedió a la página sin problemas... Se salvará como PDF")
        pyautogui.hotkey('ctrl', 'p')
        if buscar_imagen_y_clic("Save_to_PDF.png", grayscale=True, confidence=0.8):
            time.sleep(pausa)
            print(f"{mensaje_hora} Seleccionando Landscape como estilo de página")
            if buscar_imagen_y_clic("Save_to_PDF_Landscape.png", confidence=0.9):
                time.sleep(pausa)
                print(f"{mensaje_hora} Se seleccionó Landscape como estilo de página")
            else:
                print(f"{mensaje_hora} No se encontró el botón 'landscape' para elegir el estilo, quizás ya estaba seleccionado... se puede continuar")
            for _ in range(3):
                pyautogui.press('tab', interval=0.2)
            pyautogui.press('e', interval=0.2) # Seleccionar Even estilo 
            if buscar_imagen_y_clic("Save_to_PDF_Select_Click_Save_botton.png", grayscale=True, confidence=0.8):
                print(f"{mensaje_hora} Se encontró el botón 'salvar' haciendo clic")
            else:
                print(f"{mensaje_hora} No se encontró el botón 'salvar'. Bajando con teclado")
                for _ in range(4):
                    pyautogui.press('tab', interval=0.2)
                pyautogui.press('enter', interval=0.2) # Enter sobre el botón 'salvar'
                time.sleep(pausa)
            if buscar_imagen_y_clic("Save_to_PDF_Select_save_as_set_Name.png", grayscale=True, confidence=0.8):
                print(f"{mensaje_hora} Salvar como...")
                pyautogui.hotkey('ctrl', 'a') # Seleccionar todo para eliminar texto del campo de nombre
                pyautogui.typewrite(nombre_archivo)
                print(f"{mensaje_hora} Eliminando entrada y tecleando nombre {nombre_archivo}")
                time.sleep(pausa)
                pyautogui.press('enter')
                time.sleep(pausa)
            if buscar_imagen_y_clic("Save_to_PDF_as_Type_Name_Overwrite.png", grayscale=True, confidence=0.8):
                time.sleep(pausa)
                print(f"{mensaje_hora} El fichero existe, sobrescribiendo")
            if buscar_imagen_y_clic("Save_to_PDF_as_Name_final.png"):
                time.sleep(pausa)
                print(f"{mensaje_hora} Salvando el fichero {nombre_archivo}")
        if os.path.exists(nombre_archivo):
            print(f"{mensaje_hora} El fichero {nombre_archivo} existe, se salvó correctamente")
        else:
            print(f"{mensaje_hora} El fichero no existe...")
    else:
        print(f"{mensaje_hora} No se encontró la imagen 'Recently_played_Tracks.png' o no se accedió o hay algún tipo de verificación captcha")

def Recently_played_Tracks():
    """
    Esta función obtiene las estadísticas guardando la página como PDF, simulando movimientos de teclado y mouse.
    """
    # Ejecuta el comando para abrir Firefox.
    subprocess.run(firefox_command, shell=True)
    # Imprime un mensaje indicando que se va a confirmar la cuenta de correo.
    print(f"{mensaje_hora} Se van a obtener las estadisticas de la cuenta {your_username}, playlist {nombre_playlist}. Abriendo Firefox")
    # Espera 5.5 segundos para que Firefox se abra.
    time.sleep(5.5)
 
    # Verificar si se encuentra la imagen "verify_spotify_acctount_1.png"
    if buscar_imagen_y_clic("verify_spotify_acctount_Logo_Log_In.png"):
        iniciar_sesion()
        permitir_acceso_estadisticas()
        salvar_pagina_como_pdf()
    else:
        print(f"{mensaje_hora} No se pudo iniciar sesión ")

Recently_played_Tracks()

time.sleep(5.1)
from telegram_aux import enviar_archivo_telegram
import asyncio
token = "6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw"
chat_ids = ["699683569","828562504"]       # ID del Chat
archivo_configuracion = os.path.join(directorio_actual, "playlists", normalized_playlistname + ".ini")
config = configparser.ConfigParser()
config.read(archivo_configuracion)
print(f'{mensaje_hora} Directorio: {archivo_configuracion}')
# Leer los campos de la sección 'Playlist'
playlist_name = config.get('Playlist', 'nombre')
playlist_duration_minutes = int(config.get('Playlist', 'duracion'))
playlist_url = config.get('Playlist', 'url')
playlist_cover_image = config.get('Playlist', 'imagen_portada')
caption_mensaje = (f'{playlist_name}\nDuración:{playlist_duration_minutes}\nURL:\n{playlist_url}\nPortada:\n{playlist_cover_image}')
    #   Enviando Mensaje con datos de la playlist
    #loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, mensaje=caption_mensaje))
    #   Enviando Foto adjunta con caption mensaje
if os.path.exists(nombre_archivo):
    loop = asyncio.get_event_loop()
    print(f"{mensaje_hora} El fichero {nombre_archivo} existe se enviará via temegram")
    loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=nombre_archivo, caption=caption_mensaje))
    #   Enviando Archivo que contiene tracks y la informaciond e la lista
    # loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=archivo_configuracion, caption=caption_mensaje))
time.sleep(8.1)
os.remove(nombre_archivo) 
time.sleep(5.1)
pyautogui.hotkey('alt', 'f4')
