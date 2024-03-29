import time,subprocess,requests,random,os,configparser,threading,re,json,datetime
from colorama import Fore, Style
from function_utils_aux import obtener_ids_playlist, lanzar_spotify,obtener_hora_actual,minimizar_spotify,read_config

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
  
    return favorite_start_time, favorite_end_time, second_cycle_start_time, second_cycle_end_time

favorite_start_time, favorite_end_time, second_cycle_start_time, second_cycle_end_time = load_time_range()
your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, client_id, client_secret = read_config()


is_playing = False

def stop_play_spotify():
    #subprocess.run(['sp', 'stop'])
    print(f"{mensaje_hora} Stop Music!")


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


def obtener_ids_playlist():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini")) 
    playlist_ids = config.get("Play_Lists", "spotify_playlist_ids")
    playlist_ids = [id.strip() for id in playlist_ids.split(",")]
    return playlist_ids


playlist_ids = obtener_ids_playlist()
for playlist_id in playlist_ids:
    config_file = os.path.join(script_directory, "playlists", f"{playlist_id}.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    playlist_duration = int(config.get('Playlist', 'duracion'))
    playlist_name = config.get('Playlist', 'nombre')
    print(f"{mensaje_hora} {config_file}")
    print(f"ID de la lista de reproducción: {playlist_id}")
    print(f"Nombre: {playlist_name}")
    print(f"Duración: {playlist_duration}")
    print("---")

def playlist_favorite(playlist_id, playlist_history):
    global is_playing   
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    current_time = datetime.datetime.now().time()
    plus_time = 0 #random.randint(0,1) 
    random_wait_time = 0 #random.randint(0,1)
    config_file = os.path.join(script_directory, "playlists", f"{playlist_id}.ini")
    config = configparser.ConfigParser()
    config.read(config_file)

    playlist_duration = 1 #int(config.get('Playlist', 'duracion'))
    playlist_name = config.get('Playlist', 'nombre')

    start_time = datetime.datetime.now() + datetime.timedelta(minutes=random_wait_time)
    end_time = start_time + datetime.timedelta(minutes=int(playlist_duration) + plus_time)

    if playlist_id in playlist_history:
        print(f"{mensaje_hora} Playlist {playlist_name} already played in this cycle. Skipping playlist.")
        return

    stop_play_spotify()
    print(f"{mensaje_hora} Playing: {playlist_name} en {random_wait_time} segundos...")
    time.sleep(random_wait_time)

    contador_reproducciones = 0
    is_playing = True 
    print(f"{mensaje_hora} Playing Main Playlist: {playlist_name} Duration {float(playlist_duration) + plus_time} Minutes, starting at {start_time} will stop on {end_time} ")
            
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now()
                
        if is_playing and current_time.time() < end_time.time():
            print(f"{mensaje_hora} The playlist {playlist_name} stil playing. Will end at {end_time} waiting and playing, relax...")
            time.sleep(30)
            continue
                
        if current_time.time() >= end_time.time():
            print(f"{mensaje_hora} Stopping Main Playlist: {playlist_name} elapsed time {float(playlist_duration) + plus_time} Minutos end_time={end_time}")
            is_playing = False 
            stop_play_spotify()
            print(f"{mensaje_hora} Running and sending stats report for playlist:{playlist_name}...")
            time.sleep(5) # 300
            contador_reproducciones += 1
                    
            if contador_reproducciones >= 2:
                print(f"{mensaje_hora} Playlist {playlist_name} already played. Stopping and aborting.")
                stop_play_spotify()
                is_playing = False
                return
            break 
    
    playlist_history.append(playlist_id)  # Agregar el playlist_id a la lista auxiliar


def play_playlists_continuosly():
    playlist_history = []  # Lista auxiliar para almacenar las playlist_id ya reproducidas

    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()

        if is_playing:
            print(f"{mensaje_hora} Play_playlists_continuosly: Ya está reproduciéndose.{current_time} Continuando la reproducción de la lista de reproducción favorita.")
            time.sleep(30)
            continue

        if not check_time_conditions():
            playlist_ids = obtener_ids_playlist()
            playlist_ids_to_play = [playlist_id for playlist_id in playlist_ids if playlist_id not in playlist_history]  # Obtener las playlist_id que aún no se han reproducido

            if len(playlist_ids_to_play) > 0:
                playlist_id = playlist_ids_to_play[0]  # Tomar la primera playlist_id de las que aún no se han reproducido
                print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Favorite {playlist_id}.")
                playlist_favorite(playlist_id, playlist_history)
            else:
                print(f"{mensaje_hora} play_playlists_continuosly: All Playlist are played.... wait the next time.")
                break
        else:
            print(f"{mensaje_hora} play_playlists_continuosly: Nothing to play.")
            #playlist_random()
        time.sleep(60)

def verificar_playing(max_reinicios):
    while True:
        global contador_reinicios, tiempo_inicial, cancion_anterior
        while contador_reinicios < max_reinicios:
            obtener_hora_actual()
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            cancion_actual = obtener_cancion_actual()
            current_time = datetime.datetime.now().time()
            if not is_playing:
                print(f"{mensaje_hora} Is not time to play music! ")
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


def main():

    hilo_playlist = threading.Thread(target=play_playlists_continuosly)
    #hilo_verificar_playing = threading.Thread(target=verificar_playing, args=(4,))

    hilo_playlist.start()
    #hilo_verificar_playing.start()

    hilo_playlist.join()
    #hilo_verificar_playing.join()

if __name__ == "__main__":
    main()