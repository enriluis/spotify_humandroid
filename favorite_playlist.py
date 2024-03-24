import time,subprocess,requests,random,os,configparser,threading,re,json,datetime
from colorama import Fore, Style
from function_utils_aux import lanzar_spotify,obtener_hora_actual,connect_vpn_randomly,minimizar_spotify,read_config

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
script_directory = os.path.dirname(os.path.abspath(__file__))

def verificar_y_abrir_spotify():
    if not verificar_spotify():
        print(f"{mensaje_hora} Spotify no está en ejecución. Abriendo Spotify...")
        lanzar_spotify()
        time.sleep(5)
        #connect_vpn_randomly()
        minimizar_spotify()
    else:
        print(f"{mensaje_hora} Spotify ya esta ejecutandose...")


# Verificar si Spotify está en ejecución
def verificar_spotify():
    try:
        # Verificar si Spotify está en ejecución
        subprocess.check_output(['pidof', 'spotify'])
        return True
    except subprocess.CalledProcessError:
        return False


#   Reiniciar Spotify
def reset_spotify_app():
    subprocess.run(['pkill', 'spotify'])
    time.sleep(1)
    lanzar_spotify()


your_username, your_password,fecha_creacion, playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()


from playlist_info import obtener_info_playlist_from_spotify

archivo_configuracion = os.path.join(script_directory, "playlists", playlist_id + ".ini")
config = configparser.ConfigParser().read(archivo_configuracion)
playlist_duration = int(config.get('Playlist', 'duracion'))

def playlist_favorite(): 
    obtener_info_playlist_from_spotify(playlist_id)
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    current_time = datetime.datetime.now().time()
    plus_time = random.randint(3, 15)  # Tiempo adicional en minutos que se sumará a la duración
    random_wait_time = random.randint(5, 20)  # Tiempo de espera aleatorio en minutos antes de comenzar la reproducción
    start_time = datetime.datetime.now() + datetime.timedelta(minutes=random_wait_time)  # Obtener el tiempo actual y agregar el tiempo de espera
    end_time = start_time + datetime.timedelta(minutes=int(playlist_duration) + plus_time)  # Calcular el tiempo de finalización sumando la duración total y el tiempo adicional 
    
    print(f"{mensaje_hora} Playing: {nombre_playlist} en {random_wait_time} segundos...")
    time.sleep(random_wait_time)  # Convertir el tiempo de espera a segundos
    
    subprocess.run(['sp', 'open', f'spotify:playlist:{playlist_id}'])
    print(f"{mensaje_hora} Playing Main Playlist: {nombre_playlist} Duration {float(playlist_duration) + plus_time} Minutos, iniciando a las {start_time} y se detendrá a las {end_time} ")        
    subprocess.run(['sp', 'pause']) 
    subprocess.run(['sp', 'play']) 
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now()  # Actualizar el tiempo actual utilizando datetime.now()
            
        if current_time >= end_time:
            print(f"{mensaje_hora} Stopping Main Playlist: {nombre_playlist} pasado {float(playlist_duration) + plus_time} Minutos end_time={end_time}")
            subprocess.run(['sp', 'stop'])
            estadisticas_script = os.path.join(script_directory, 'estadisticas.py')
            subprocess.run(['python3', estadisticas_script, playlist_id, str(nombre_playlist), str(playlist_duration)])            
            time.sleep(300)    # ciclo que comprueba a duracion de la reproduccion de favorite playlist
            break

verificar_y_abrir_spotify() 
time.sleep(5.1)       
subprocess.run(['vpn-con-rand'])
playlist_favorite()

print(f"{mensaje_hora} Continuar con el monitoreo normal...")
time.sleep(300)

spotify_monitor = os.path.join(script_directory, 'spotify_monitor.py')
subprocess.run(['python3', spotify_monitor])

