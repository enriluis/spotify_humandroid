import time,subprocess,requests,random,os,configparser,threading,re,json,datetime
from colorama import Fore, Style
from function_utils_aux import obtener_ids_playlist, lanzar_spotify,obtener_hora_actual,minimizar_spotify,read_config
from playlist_info import obtener_info_playlist_from_spotify
import os
os.environ['DISPLAY'] = ':0.0'
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"


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
        time.sleep(8.102)
        minimizar_spotify()
    else:
        print(f"{mensaje_hora} Spotify already running...")


def verificar_spotify():
    try:
        subprocess.check_output(['pidof', 'spotify'])
        return True
    except subprocess.CalledProcessError:
        return False

def kill_spotify_app():
    subprocess.run(['pkill', 'spotify'])
    time.sleep(1)


def parse_time(time_str):
    return datetime.datetime.strptime(time_str, "%H:%M").time()

def load_scheduled_hours_day():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))    
    scheduled_hours_day = config["scheduled_time"]["scheduled_hours"].replace(" ", "").split(",")

    formatted_hours_day = []
    for hour in scheduled_hours_day:
        hour_parts = hour.split(":")
        formatted_hour = f"{hour_parts[0].zfill(2)}:{hour_parts[1].zfill(2)}:00"
        formatted_hours_day.append(formatted_hour)

    if len(formatted_hours_day) > 4:
        print(f"{mensaje_hora} Warning there is more than 4 values of time to schedule, will be ignored the other values")
        
    scheduled_hours_day = formatted_hours_day[:4]  # Limitar a 4 valores

    return scheduled_hours_day

scheduled_hours_day = load_scheduled_hours_day()
your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, client_id, client_secret = read_config()


is_playing = False

def stop_play_spotify():
    random_delay_ms = random.randint(100, 500)
    time.sleep(random_delay_ms / 1000)
    print(f"{mensaje_hora} Stop Music in {random_delay_ms}ms")
    subprocess.run(['sp', 'stop'])


def obtener_ids_playlist():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini")) 
    playlist_ids = config.get("Play_Lists", "spotify_playlist_ids")
    playlist_ids = [id.strip() for id in playlist_ids.replace(" ", "").split(",")]

    if len(playlist_ids) > 4:
        print(f"{mensaje_hora} Warning: There are more than 4 playlist_id values. The other values will be ignored!!")

    valid_playlist_ids = []
    for playlist_id in playlist_ids:
        if len(playlist_id) == 22 and playlist_id.isalnum():
            valid_playlist_ids.append(playlist_id)
        else:
            print(f"{mensaje_hora} Warning: The playlist_id '{playlist_id}' does not meet the required length of 22 characters. It has {len(playlist_id)} characters.")

    playlist_ids = valid_playlist_ids[:4]
    return playlist_ids


playlist_ids = obtener_ids_playlist()

for playlist_id in playlist_ids:
    time_threshold = 24 * 60 * 60  # 24 hours in seconds
    config_file = os.path.join(script_directory, "playlists", f"{playlist_id}.ini")
    if os.path.exists(config_file):
        print(f"{mensaje_hora} File exists for playlist ID:", playlist_id) 
        modification_time = os.path.getmtime(config_file)
        current_time = time.time()
        time_difference = current_time - modification_time

        if time_difference > time_threshold:
            print(f"{mensaje_hora} File is older than 24 hours for playlist ID:", playlist_id)
            obtener_info_playlist_from_spotify(playlist_id)        
        
    else:
        print(f"{mensaje_hora} File does not exist for playlist ID:", playlist_id)
        print(f"{mensaje_hora} Downloading playlist info from Spotify API ID:", playlist_id)
        obtener_info_playlist_from_spotify(playlist_id)
               
    config = configparser.ConfigParser()
    config.read(config_file)
    playlist_duration = int(config.get('Playlist', 'duration'))
    playlist_name = config.get('Playlist', 'name')
    print(f"{mensaje_hora} {config_file}")
    print(f"{mensaje_hora} Playlist ID: {playlist_id}")
    print(f"{mensaje_hora} Name: {playlist_name}")
    print(f"{mensaje_hora} Duration: {playlist_duration}")
    print(f"{mensaje_hora} ---")

    
def playlist_favorite(playlist_id):
    global is_playing   
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    verificar_y_abrir_spotify()
    current_time = datetime.datetime.now().time()
    plus_time = random.randint(3, 15)
    random_wait_time = random.randint(5, 20)
    random_delay_ms_start = random.randint(1000, 8000)  
    random_delay_ms_end = random.randint(2000, 11000)
    config_file = os.path.join(script_directory, "playlists", f"{playlist_id}.ini")      
    config = configparser.ConfigParser()
    config.read(config_file)    
    playlist_duration = int(config.get('Playlist', 'duration'))
    start_time = datetime.datetime.now() + datetime.timedelta(minutes=random_wait_time)
    start_time += datetime.timedelta(milliseconds=random_delay_ms_start)  
    end_time = start_time + datetime.timedelta(minutes=int(playlist_duration) + plus_time)
    end_time += datetime.timedelta(milliseconds=random_delay_ms_end) 


    playlist_name =f"{Fore.LIGHTBLUE_EX}{config.get('Playlist', 'name')}{Style.RESET_ALL}"

    stop_play_spotify()
    print(f"{mensaje_hora} Playing: {playlist_name} en {random_wait_time} segundos...")
    time.sleep(random_wait_time)

    contador_reproducciones = 0
    is_playing = True 
    subprocess.run(['sp', 'open', f'spotify:playlist:{playlist_id}'])
    control_verificacion_reproduccion()  # Llamada a la función para iniciar la verificación

    print(f"{mensaje_hora} Playing Main Playlist: {playlist_name} Duration {float(playlist_duration) + plus_time} Minutes, starting at {start_time} will stop on {end_time} ")
            
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now()
                
        if is_playing and current_time.time() < end_time.time():
            print(f"{mensaje_hora} The playlist {playlist_name} stil playing. Will end at {end_time} waiting and playing, relax...")
            time.sleep(900)
            continue
                
        if current_time.time() >= end_time.time():
            print(f"{mensaje_hora} Stopping Main Playlist: {playlist_name} elapsed time {float(playlist_duration) + plus_time} Minutos end_time={end_time}")
            is_playing = False 
            stop_play_spotify()
            print(f"{mensaje_hora} Sending stats report for playlist: {playlist_name}...")
            kill_spotify_app()
            script_estadisticas = os.path.join(script_directory, "estadisticas.py")
            subprocess.run(['python3', script_estadisticas, playlist_id])        
            time.sleep(300) # 300
            contador_reproducciones += 1
                    
            if contador_reproducciones >= 2:
                print(f"{mensaje_hora} Playlist {playlist_name} already played. Stopping and aborting.")
                stop_play_spotify()
                is_playing = False
                control_verificacion_reproduccion()  # Llamada a la función para detener la verificación
                kill_spotify_app()
                return
            break

import schedule

def playlist_favorite_scheduler(playlist_ids):
    playlist_history = []
    scheduled_hours_day = load_scheduled_hours_day()

    def playlist_favorite_wrapper(playlist_id):
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()

        if is_playing:
            print(f"{mensaje_hora} playlist_favorite_scheduler: Already playing at {current_time}. Continuing playback of favorite playlist.")
            return

        print(f"{mensaje_hora} playlist_favorite_scheduler: Playing playlist {playlist_id}.")
        playlist_favorite(playlist_id)

    for playlist_id in playlist_ids:
        for scheduled_hour in scheduled_hours_day:
            print(f"{mensaje_hora} The playlist {playlist_id} will be played at {scheduled_hour}.")
            schedule.every().day.at(scheduled_hour).do(playlist_favorite_wrapper, playlist_id)

    while True:
        next_schedule = schedule.next_run()
        current_time = datetime.datetime.now()
        time_diff = next_schedule - current_time
        countdown_minutes = time_diff.total_seconds() / 60
        countdown_str = str(datetime.timedelta(minutes=int(countdown_minutes)))
        print(f"{mensaje_hora} Next playlist playback in: {Fore.CYAN}{countdown_str}{Style.RESET_ALL}")
        time.sleep(1)
        schedule.run_pending()


def verificar_playing(max_reinicios):
    global contador_reinicios, tiempo_inicial, cancion_anterior

    while is_playing:
        while contador_reinicios < max_reinicios:
            obtener_hora_actual()
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            cancion_actual = obtener_cancion_actual()
            current_time = datetime.datetime.now().time()

            if cancion_actual == cancion_anterior:
                if time.time() - tiempo_inicial >= 300: 
                    contador_reinicios += 1
                    print(f"{mensaje_hora} Track \u266A{titulo}\u266A has not changed after 5 minutes...")
            else:
                print(f"{mensaje_hora} Playing \u25B6: {Fore.BLUE}\u266A{titulo}\u266A{Style.RESET_ALL}, Artist{Fore.YELLOW} {artista}{Style.RESET_ALL}, Album {Fore.GREEN}{album}{Style.RESET_ALL}")
                cancion_anterior = cancion_actual
                tiempo_inicial = time.time()

        print(f"{mensaje_hora} Spotify restarted {contador_reinicios} times in 30 min")
        contador_reinicios = 0
        time.sleep(60)

import threading

verificacion_reproduccion_thread = None
def control_verificacion_reproduccion():
    global is_playing, verificacion_reproduccion_thread

    if is_playing and not verificacion_reproduccion_thread:
        # Comenzar la verificación de reproducción en un hilo separado
        verificacion_reproduccion_thread = threading.Thread(target=verificar_playing, args=(4,))
        verificacion_reproduccion_thread.start()
    elif not is_playing and verificacion_reproduccion_thread:
        # Detener la verificación de reproducción
        verificacion_reproduccion_thread.join()
        verificacion_reproduccion_thread = None


def main():
    #verificar_y_abrir_spotify()
    playlist_ids = obtener_ids_playlist()

    playlist_thread = threading.Thread(target=playlist_favorite_scheduler, args=(playlist_ids,))
    playlist_thread.start()

if __name__ == "__main__":
    main()