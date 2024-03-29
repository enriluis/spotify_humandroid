import time,subprocess,requests,random,os,configparser,threading,re,json,datetime
from colorama import Fore, Style
from function_utils_aux import obtener_ids_playlist, lanzar_spotify,obtener_hora_actual,connect_vpn_randomly,minimizar_spotify,read_config,obtener_info_playlist

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
# Declarar las variables globales
titulo = ""
artista = ""
album_artista = ""
album = ""
contador_reinicios = 0
cancion_anterior = ""

script_directory = os.path.dirname(os.path.abspath(__file__))

def obtener_cancion_actual():
    obtener_hora_actual()
    global titulo, artista, album_artista, album 
    result = subprocess.run(['sp', 'current'], capture_output=True, text=True)
    output = result.stdout.strip()    
    lines = output.split('\n')
    song_info = {}
    for line in lines:   
        if line:
            key_value = line.split(maxsplit=1)
            if len(key_value) == 2:
                key, value = key_value
                song_info[key] = value
    titulo = song_info.get('Title', '')
    artista = song_info.get('Artist', '')
    album_artista = song_info.get('AlbumArtist', '')
    album = song_info.get('Album', '')
    return song_info


def verificar_y_abrir_spotify():
    if not verificar_spotify():
        print(f"{mensaje_hora} Spotify no está en ejecución. Abriendo Spotify...")
        lanzar_spotify()
        time.sleep(5)
        subprocess.run(['vpn-con-rand'])
        minimizar_spotify()
    else:
        print(f"{mensaje_hora} Spotify ya esta ejecutandose...")


def verificar_spotify():
    try:
        subprocess.check_output(['pidof', 'spotify'])
        return True
    except subprocess.CalledProcessError:
        return False

def reset_spotify_app():
    subprocess.run(['pkill', 'spotify'])
    time.sleep(1)
    lanzar_spotify()  

def parse_time(time_str):
    return datetime.datetime.strptime(time_str, "%H:%M").time()

def load_time_range():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))    
    favorite_start_time = parse_time(config["favorite_times"]["favorite_start_time"])
    favorite_end_time = parse_time(config["favorite_times"]["favorite_end_time"])
    second_cycle_start_time = parse_time(config["second_cycle_times"]["second_cycle_start_time"])
    second_cycle_end_time = parse_time(config["second_cycle_times"]["second_cycle_end_time"])
    break_start_time = parse_time(config["break_times"]["break_start_time"])
    break_end_time = parse_time(config["break_times"]["break_end_time"])    
    return favorite_start_time, favorite_end_time, second_cycle_start_time, second_cycle_end_time, break_start_time, break_end_time

favorite_start_time, favorite_end_time, second_cycle_start_time, second_cycle_end_time, break_start_time, break_end_time = load_time_range()
your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, client_id, client_secret = read_config()
playlist_id = obtener_ids_playlist() 

is_playing = False

def is_break_time(break_start_time, break_end_time):
    obtener_hora_actual()
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    current_date = current_datetime.date()    
    if break_start_time <= current_time or current_time <= break_end_time:
        if current_time <= break_end_time and current_date == datetime.date.today():
            #print(f"{mensaje_hora} It's break time {current_time}-{current_date}!")
            return True
        elif current_time >= break_start_time and current_date == datetime.date.today():
            #print(f"{mensaje_hora} It's break time {current_time}-{current_date}!")
            return True
        else:
            #print(f"{mensaje_hora} No break time right now {current_time}-{current_date}.")
            return False
    else:
        #print(f"{mensaje_hora} No break time right now {current_time}-{current_date}.")
        return False

def check_time_conditions():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    current_datetime = datetime.datetime.now()
    current_time = current_datetime.time()
    if (favorite_start_time <= current_time <= favorite_end_time) or \
        (second_cycle_start_time <= current_time <= second_cycle_end_time): 
        print(f"{mensaje_hora} Check Time conditions: Favorite Playlist time  to play: {Fore.LIGHTGREEN_EX}{favorite_start_time} \u25B6 {favorite_end_time}{Style.RESET_ALL} y {Fore.LIGHTGREEN_EX}{second_cycle_start_time} \u25B6 {second_cycle_end_time}{Style.RESET_ALL} ")
        return True
    else:
        print(f"{mensaje_hora} Check Time conditions: No Favorite  Playlist time {favorite_start_time} <= {current_time} <= {second_cycle_end_time} ")
        return False


def playlist_random():
    archivo_entrada = os.path.join(os.path.dirname(__file__), "random_playlist.txt")
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()
        if is_playing:
            print(f"{mensaje_hora} \u266Aplay_playlists_continuosly: \u25B6 Ya esta reproduciendose \u266A Continuando la reproducción de la lista de reproducción favorita\u266A.")
            time.sleep(300)
            continue
        if (break_start_time <= current_time <= break_end_time) \
            or (break_start_time > break_end_time and (current_time >= break_start_time or current_time <= break_end_time)):
            print(f"{mensaje_hora} Break time. Stopping \u23F9 Random Playlist\u266A.")
            subprocess.run(['sp', 'stop'])
            break
        elif favorite_start_time <= current_time <= favorite_end_time:
            print(f"{mensaje_hora} Favorite first time. Stopping \u23F9 Random Playlist\u266A.")
            subprocess.run(['sp', 'stop'])
            break
        elif second_cycle_start_time <= current_time <= second_cycle_end_time:
            print(f"{mensaje_hora} Second cicle Favorite pl. time Stopping \u23F9 Random Playlist\u266A.")
            subprocess.run(['sp', 'stop'])
            break
        else:
            print(f"{mensaje_hora} Hora de reproducir \u25B6 Playlist Random playlist. \u266A")
            with open(archivo_entrada, "r") as archivo:
                lineas = archivo.readlines()
            id_elegido = random.choice(lineas).strip()     
            print(f"{mensaje_hora} Cambiando de Play List random reproduciendo: \u266A {id_elegido} \u266A")
            print(f"    {favorite_start_time}       <=      {current_time}      <=      {favorite_end_time} ")
            print(f"    {second_cycle_start_time}   <=      {current_time}      <=      {second_cycle_end_time} ")
            #subprocess.run(['sp', 'open', f'spotify:playlist:{id_elegido}'])
            rotate_time = random.randint(39, 59) * 60
            time.sleep(rotate_time)

from playlist_info import obtener_info_playlist_from_spotify

archivo_configuracion = os.path.join(script_directory, "playlists", f"{playlist_id}.ini")
config = configparser.ConfigParser().read(archivo_configuracion)
playlist_duration = int(config.get('Playlist', 'duration'))
playlist_name = config.get('Playlist', 'playlist_name')
playlist_ids = obtener_ids_playlist()

def playlist_favorite(playlist_id):
    for playlist_id in playlist_ids:
        obtener_info_playlist_from_spotify(playlist_id)
        global is_playing   
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()
        plus_time = random.randint(3, 15) 
        random_wait_time = random.randint(5, 20)
        start_time = datetime.datetime.now() + datetime.timedelta(minutes=random_wait_time)
        end_time = start_time + datetime.timedelta(minutes=int(playlist_duration) + plus_time)
        subprocess.run(['sp', 'stop'])
        print(f"{mensaje_hora} Playing: {playlist_name} en {random_wait_time} segundos...")
        time.sleep(random_wait_time)
        
        contador_reproducciones = 0
        is_playing = True 
        subprocess.run(['sp', 'open', f'spotify:playlist:{playlist_id}'])
        print(f"{mensaje_hora} Playing Main Playlist: {playlist_name} Duration {float(playlist_duration) + plus_time} Minutes, starting at {start_time} will stop on {end_time} ")
            
        while True:
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            current_time = datetime.datetime.now()
                
            if is_playing and current_time.time() < end_time.time():
                print(f"{mensaje_hora} the playlyist {playlist_name} stil playing. Will end at {end_time} waiting and playin, relax...")
                time.sleep(900)
                continue
                
            if current_time.time() >= end_time.time():
                print(f"{mensaje_hora} Stopping Main Playlist: {playlist_name} elapsed time {float(playlist_duration) + plus_time} Minutos end_time={end_time}")
                is_playing = False 
                subprocess.run(['sp', 'stop'])
                print(f"{mensaje_hora} Running and sending stats report {playlist_name}...")
                estadisticas_script = os.path.join(script_directory, 'estadisticas.py')
                subprocess.run(['python3', estadisticas_script, playlist_id, str(playlist_name), str(playlist_duration)])
                    
                time.sleep(300)
                contador_reproducciones += 1
                    
                if contador_reproducciones >= 2:
                    print(f"{mensaje_hora} Playlist {playlist_name} already played. Stoping and aborting .")
                    subprocess.run(['sp', 'stop'])
                    is_playing = False
                    return
                break 
        

def play_playlists_continuosly():
    playlist_ids = obtener_ids_playlist()  # Obtener los IDs de las listas de reproducción

    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()

        if is_playing:
            print(f"{mensaje_hora} play_playlists_continuosly: Ya está reproduciéndose.{current_time} Continuando la reproducción de la lista de reproducción favorita.")
            time.sleep(300)
            continue

        if check_time_conditions():
            for playlist_id in playlist_ids:
                print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Favorite {playlist_id}.")
                playlist_favorite(playlist_id)  # Llamar la función playlist_favorite() con cada ID de lista de reproducción
        else:
            print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Random.")
            playlist_random()
        time.sleep(900)

def play_playlists_continuosly_old():
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()
        if is_playing:
            print(f"{mensaje_hora} play_playlists_continuosly: Ya esta reproduciendose.{current_time} Continuando la reproducción de la lista de reproducción favorita.")
            time.sleep(300) 
            continue

        if check_time_conditions():
            print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Favorite {playlist_name} .")
            playlist_favorite(playlist_id)
        else:
            print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Random.")
            playlist_random()
        time.sleep(900)


def verificar_playing(max_reinicios):
    while True:
        global contador_reinicios, tiempo_inicial, cancion_anterior
        while contador_reinicios < max_reinicios:
            obtener_hora_actual()
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            cancion_actual = obtener_cancion_actual()
            current_time = datetime.datetime.now().time()
            if (break_start_time <= current_time <= break_end_time) \
                or (break_start_time > break_end_time and (current_time >= break_start_time or current_time <= break_end_time)):
                print(f"{mensaje_hora} Time Sleep, nothing to check")
                continue
            if cancion_actual == cancion_anterior:
                if time.time() - tiempo_inicial >= 300: 
                    contador_reinicios += 1
                    print(f"{mensaje_hora} Track \u266A{titulo}\u266A has no changed afther 5 minutes...")
                    
            else:
                print(f"{mensaje_hora} Playing \u25B6: {Fore.BLUE}\u266A{titulo}\u266A{Style.RESET_ALL}, Artist{Fore.YELLOW} {artista}{Style.RESET_ALL}, Album {Fore.GREEN}{album}{Style.RESET_ALL}")
                cancion_anterior = cancion_actual
                tiempo_inicial = time.time() 
        print(f"{mensaje_hora} Spotify restarted {contador_reinicios} times in 30 min")
        contador_reinicios = 0            
        time.sleep(60) 

def verificar_conexion():
    while True:
        obtener_hora_actual()
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        time.sleep(900) 
        if not requests.get('https://www.google.com', timeout=5).status_code == 200:
            print(f"{mensaje_hora} La conexión a internet ha fallado. Ejecutando comando...")        
            #connect_vpn_randomly() 
            return False
        else:
            print(f"{mensaje_hora} La conexion Esta OK")
            return True

fecha_creacion_str = creation_date
def calcular_edad_cuenta():
    creation_date = datetime.datetime.strptime(fecha_creacion_str, "%Y-%m-%d %H:%M:%S.%f")
    today_date = datetime.datetime.now()
    diferencia = today_date - creation_date
    edad_dias = diferencia.days
    edad_horas = diferencia.seconds // 3600
    return edad_dias, edad_horas

edad_dias, edad_horas = calcular_edad_cuenta()
print(f"{mensaje_hora} Edad de la cuenta {your_username}: {edad_dias} días y {edad_horas} horas")

def verificacion_edad_cuenta():
    # Bucle para ejecutar las tareas programadas
    while True:
        edad_dias, edad_horas = calcular_edad_cuenta()
        print(f"{mensaje_hora} Edad de la cuenta {your_username}: {edad_dias} días y {edad_horas} horas")
        
        if edad_dias == 6 and edad_horas == 12:
            print(f"{mensaje_hora} La cuenta tiene 6 días y 12 horas de edad. se crera una nueva cuenta...")

        time.sleep(12 * 60 * 60)    # 12horas=12 * 60 * 60

script_directory = os.path.dirname(os.path.abspath(__file__))
import pyautogui
def buscar_imagen_en_pantalla(image_path, num_intentos=15, timeout=30, **kwargs):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    start_time = time.time()
    ruta_completa = os.path.join(script_directory, 'images', image_path) 
    for i in range(num_intentos):
        match = pyautogui.locateOnScreen(ruta_completa, **kwargs)
        if match:

            image_location = pyautogui.center(match)
            #pyautogui.click(image_location)
            print(f"{mensaje_hora} Encontrada la imagen {image_path} en captura {i+1} de {num_intentos}, haciendo clic...")
            return True, image_location
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            return False, None
        time.sleep(1)
    print(f"{mensaje_hora} No encontró imagen {image_path} ...")
    return False, None

from function_utils_aux import maximizar_spotify  
from telegram_aux import enviar_archivo_telegram 
import asyncio

def taket_screenshot_send_telegram():
    loop = asyncio.get_event_loop()
    token = "6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw"
    chat_ids = ["699683569"]#,"828562504"] 
    screenshot = pyautogui.screenshot()
    now = datetime.datetime.now() 
    timestamp = now.strftime("%d-%m-%Y_%H-%M")
    screenshot_image = "{}_{}.png".format(playlist_id, timestamp)
    screenshot.save(screenshot_image)
    print(f"{mensaje_hora} salvando captura...")
    #loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, mensaje=caption_mensaje))
    time.sleep(6.1)
    minimizar_spotify()
    caption_mensaje = (f'Captura de pantalla Spotify')
    loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=screenshot_image, caption=caption_mensaje))
    print(f"{mensaje_hora} Enviando captura...")
    time.sleep(8.1)
    os.remove(screenshot_image)   

def verify_session_spotify():
    while True:
        obtener_hora_actual()
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        maximizar_spotify()
        time.sleep(2.1)
        time.sleep(12 * 60 * 60)
        if buscar_imagen_en_pantalla("spotify_is_playing_ok.png"):
            print(f"{mensaje_hora} spotify esta abierto, la cuenta esta OK...")                    
            minimizar_spotify() 
        else:
            print(f"{mensaje_hora} No se encontró la imagen, parece que spotify no esta corriendo o la sesion no esta abierta")
            taket_screenshot_send_telegram()
            print(f"{mensaje_hora} Se creará una nueva cuenta...")


def main():
    verificar_y_abrir_spotify()
    hilo_playlist = threading.Thread(target=play_playlists_continuosly)
    hilo_verificar_playing = threading.Thread(target=verificar_playing, args=(4,))
    hilo_verificar_conexion = threading.Thread(target=verificar_conexion)
    hilo_edad_cuenta = threading.Thread(target=verificacion_edad_cuenta)
    hilo_spotify_playing = threading.Thread(target=verify_session_spotify)

    hilo_playlist.start()
    hilo_verificar_playing.start()
    hilo_verificar_conexion.start()
    hilo_edad_cuenta.start()
    hilo_spotify_playing.start()

    hilo_playlist.join()
    hilo_verificar_playing.join()
    hilo_verificar_conexion.join()
    hilo_edad_cuenta.join()
    hilo_spotify_playing.join()

if __name__ == "__main__":
    main()