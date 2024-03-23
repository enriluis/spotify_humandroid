import time,subprocess,requests,random,os,configparser,threading,re,datetime
from colorama import Fore, Style
from function_utils_aux import register_spotify_account,lanzar_spotify,obtener_hora_actual,connect_vpn_randomly,minimizar_spotify,read_config

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
# Declarar las variables globales
titulo = ""
artista = ""
album_artista = ""
album = ""
contador_reinicios = 0
cancion_anterior = ""
tiempo_inicial = time.time()
current_time = datetime.datetime.now()
def obtener_cancion_actual():
    obtener_hora_actual()
    global titulo, artista, album_artista, album  # Indicar que estamos utilizando las variables globales
    result = subprocess.run(['sp', 'current'], capture_output=True, text=True)
    output = result.stdout.strip()    
    lines = output.split('\n')  # Dividir las líneas del resultado en una lista de líneas
    song_info = {}              # Crear un diccionario para almacenar los valores
    for line in lines:          # Iterar a través de las líneas y extraer los datos
        if line:
            key_value = line.split(maxsplit=1)
            if len(key_value) == 2:
                key, value = key_value
                song_info[key] = value
    titulo = song_info.get('Title', '')    # Asignar los valores globales
    artista = song_info.get('Artist', '')
    album_artista = song_info.get('AlbumArtist', '')
    album = song_info.get('Album', '')
    return song_info


def verificar_y_abrir_spotify():
    if not verificar_spotify():
        print(f"{mensaje_hora} Spotify no está en ejecución. Abriendo Spotify...")
        lanzar_spotify()
        time.sleep(5)
        connect_vpn_randomly()
        minimizar_spotify()
    else:
        print(f"{mensaje_hora} Spotify ya esta ejecutandose...")
        connect_vpn_randomly()
        #subprocess.run(['sp', 'play'])

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
    #subprocess.run(['sp', 'play'])   

import datetime 
current_time = datetime.datetime.now().time()
favorite_start_time = datetime.datetime.strptime("19:10", "%H:%M").time()
favorite_end_time = datetime.datetime.strptime("19:15", "%H:%M").time()
second_cycle_start_time = datetime.datetime.strptime("19:37", "%H:%M").time()
second_cycle_end_time = datetime.datetime.strptime("19:41", "%H:%M").time()
break_start_time = datetime.datetime.strptime("19:20", "%H:%M").time()  # Hora de inicio del descanso
break_end_time = datetime.datetime.strptime("19:30", "%H:%M").time()  # Hora de fin del descanso

your_username, your_password, fecha_creacion, playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()
is_playing = False  # Declaración de la variable global


def playlist_random():
    #archivo_entrada = "/home/lmb/spotify/random_playlist.txt"
    archivo_entrada = "D:\\Users\\rancher\\Documents\\YIYO-LMB\\spotify_project\\spotify-develop-normal\\random_playlist.txt"
    while True:
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        current_time = datetime.datetime.now().time()
        if is_playing:
            print(f"{mensaje_hora} \u266Aplay_playlists_continuosly: \u25B6 Ya esta reproduciendose \u266A Continuando la reproducción de la lista de reproducción favorita\u266A.")
            time.sleep(30)  # Esperar 5 minuto antes de realizar el siguiente chequeo
            continue
        if (break_start_time <= current_time <= break_end_time) \
            or (break_start_time > break_end_time and (current_time >= break_start_time or current_time <= break_end_time)):
            # El bloque de código correspondiente al tiempo de descanso
            print(f"{mensaje_hora} Break time. Stopping \u23F9 Random Playlist\u266A.")
            #subprocess.run(['sp', 'stop'])
            break
        elif favorite_start_time <= current_time <= favorite_end_time:
            # El bloque de código correspondiente al horario favorito
            print(f"{mensaje_hora} Favorite first time. Stopping \u23F9 Random Playlist\u266A.")
            #subprocess.run(['sp', 'stop'])
            break
        elif second_cycle_start_time <= current_time <= second_cycle_end_time:
            # El bloque de código correspondiente al segundo ciclo
            print(f"{mensaje_hora} Second cicle Favorite pl. time Stopping \u23F9 Random Playlist\u266A.")
            #subprocess.run(['sp', 'stop'])
            break
        else:
            print(f"{mensaje_hora} Hora de reproducir \u25B6 Playlist Random playlist. \u266A")
            with open(archivo_entrada, "r") as archivo:
                lineas = archivo.readlines()
            id_elegido = random.choice(lineas).strip()     
            print(f"{mensaje_hora} Cambiando de Play List random reproduciendo: \u266A {id_elegido} \u266A")
            #subprocess.run(['sp', 'open', f'spotify:playlist:{id_elegido}'])
            rotate_time = random.randint(5, 10) #* 60
            time.sleep(rotate_time)

        

def playlist_favorite():
    global is_playing   
    playlist_duration = 1
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    current_time = datetime.datetime.now().time()
    plus_time = random.randint(1, 2)  # Tiempo adicional en minutos que se sumará a la duración
    random_wait_time = random.randint(1, 5)  # Tiempo de espera aleatorio en minutos antes de comenzar la reproducción
    start_time = datetime.datetime.now() + datetime.timedelta(minutes=random_wait_time)  # Obtener el tiempo actual y agregar el tiempo de espera
    end_time = start_time + datetime.timedelta(minutes=int(playlist_duration) + plus_time)  # Calcular el tiempo de finalización sumando la duración total y el tiempo adicional
    #subprocess.run(['sp', 'stop'])   
    print(f"{mensaje_hora} Playing: {nombre_playlist} en {random_wait_time} segundos...")
    #time.sleep(random_wait_time)  # Convertir el tiempo de espera a segundos
    
    if check_time_conditions():
        contador_reproducciones = 0
        is_playing = True  # Establecer la variable de estado a True
        #subprocess.run(['sp', 'open', f'spotify:playlist:{playlist_id}'])
        print(f"{mensaje_hora} Playing Main Playlist: {nombre_playlist} Duration {float(playlist_duration) + plus_time} Minutos, iniciando a las {start_time} y se detendrá a las {end_time} ")        
        while True:
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            current_time = datetime.datetime.now()  # Actualizar el tiempo actual utilizando datetime.now()
            
            if is_playing and current_time.time() < end_time.time():
                print(f"{mensaje_hora} La lista de reproducción favorita todavía está en reproducción. Esperando...")
                time.sleep(60)  # Esperar 1 minuto antes de verificar nuevamente # poner 300, 5 minutos
                continue  # Volver al inicio del bucle sin ejecutar más código
            
            if current_time.time() >= end_time.time():
                print(f"{mensaje_hora} Stopping Main Playlist: {nombre_playlist} pasado {float(playlist_duration) + plus_time} Minutos end_time={end_time}")
                is_playing = False  # Establecer la variable de estado a False
                #subprocess.run(['sp', 'stop'])
                print(f"{mensaje_hora} Ejecutando estadísticas para la playlist {nombre_playlist}...")
                #subprocess.run(['python3', '/home/lmb/spotify/estadisticas.py']) 
                time.sleep(30)    # ciclo que comprueba a duracion de la reproduccion de favorite playlist
                contador_reproducciones += 1
                if contador_reproducciones >= 2:  # Verificar si la playlist ya se reprodujo más de una vez
                    print(f"{mensaje_hora} Playlist {nombre_playlist} already played. Stoping and aborting .")
                    subprocess.run(['sp', 'stop'])
                    is_playing = False
                    return  # Abortar la función sin continuar con el ciclo
                break
    else:
        print(f"{mensaje_hora} Hora de descansar...") 
        is_playing = False  # Establecer la variable de estado a False
        subprocess.run(['sp', 'stop'])



def check_time_conditions():
    current_time = datetime.datetime.now().time()
    if (favorite_start_time <= current_time <= favorite_end_time) or \
        (second_cycle_start_time <= current_time <= second_cycle_end_time):       
        return True
    else:
        print(f"{mensaje_hora} La hora actual no se corresponde para reproducir Favorite ")
        return False
    
def play_playlists_continuosly():
    while True:
        if is_playing:
            print(f"{mensaje_hora} play_playlists_continuosly: Ya esta reproduciendose. Continuando la reproducción de la lista de reproducción favorita.")
            time.sleep(60)  # Esperar 1 minuto antes de realizar el siguiente chequeo
            continue  # Saltar a la siguiente iteración del bucle sin ejecutar más código

        if check_time_conditions():
            print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Favorite.")
            playlist_favorite()
        else:
            print(f"{mensaje_hora} play_playlists_continuosly: Reproducirá Random.")
            playlist_random()
        time.sleep(60)  # Esperar 1 minuto antes de realizar el siguiente chequeo

def verificar_playing(max_reinicios):
    while True:
        global contador_reinicios, tiempo_inicial, cancion_anterior
        while contador_reinicios < max_reinicios:
            obtener_hora_actual()
            mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
            cancion_actual = obtener_cancion_actual()
            time.sleep(60)  # Esperar 1 minuto
            if cancion_actual == cancion_anterior:
                if time.time() - tiempo_inicial >= 2100:  # Han pasado 5 minutos
                    contador_reinicios += 1
                    print(f"{mensaje_hora} La canción {titulo} no ha cambiado pasado 7 minutos. {Fore.RED}Reiniciando Spotify{Style.RESET_ALL}...")
                    #reset_spotify_app()
            else:
                print(f"{mensaje_hora} Playing: {Fore.BLUE}{titulo}{Style.RESET_ALL}, Artist{Fore.YELLOW} {artista}{Style.RESET_ALL}, Album {Fore.GREEN}{album}{Style.RESET_ALL}")
                cancion_anterior = cancion_actual
                tiempo_inicial = time.time() 
        print(f"{mensaje_hora} Spotify restarted {contador_reinicios} times in 30 min")
        contador_reinicios = 0            
        print(f"{mensaje_hora} Verificando que las tareas se estén ejecutando")
        time.sleep(60)  
        print(f"{mensaje_hora} Verificación completa")

def verificar_conexion():
    while True:
        obtener_hora_actual()
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        time.sleep(900)  # Esperar 15 minutos
        if not requests.get('https://www.google.com', timeout=5).status_code == 200:
            print(f"{mensaje_hora} La conexión a internet ha fallado. Ejecutando comando...")        
            connect_vpn_randomly()    # Ejecutar el comando que deseas al fallar la conexión
            return False
        else:
            print(f"{mensaje_hora} La conexion Esta OK")
            return True
# Verificar si esta pinchando spotify y enciar captura por telegram.
# Obtener la ruta absoluta del directorio del script
script_directory = os.path.dirname(os.path.abspath(__file__))
import pyautogui
def buscar_imagen_en_pantalla(image_path, num_intentos=15, timeout=30, **kwargs):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    start_time = time.time()
    ruta_completa = os.path.join(script_directory, 'images', image_path)  # Ruta completa de la imagen
    for i in range(num_intentos):
        match = pyautogui.locateOnScreen(ruta_completa, **kwargs)
        if match:
            # La imagen se encontró, hacer clic en ella
            image_location = pyautogui.center(match)
            #pyautogui.click(image_location)
            print(f"{mensaje_hora} Encontrada la imagen {image_path} en captura {i+1} de {num_intentos}, haciendo clic...")
            return True, image_location
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            # Se agotó el tiempo de espera para encontrar la imagen
            return False, None
        time.sleep(1)
    # No se encontró la imagen después de los intentos
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
    normalized_filename = re.sub(r'[^\w\-_.]', '', nombre_playlist)
    screenshot_image = "{}_{}.png".format(normalized_filename, timestamp)
    screenshot.save(screenshot_image)
    print(f"{mensaje_hora} salvando captura...")
    #loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, mensaje=caption_mensaje))
    time.sleep(6.1)
    minimizar_spotify()
    caption_mensaje = (f'Captura de pantalla Spotify')
    loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=screenshot_image, caption=caption_mensaje))
    print(f"{mensaje_hora} Enviando captura...")
    # Eliminar el archivo de imagen después de enviarlo
    time.sleep(8.1)
    os.remove(screenshot_image)   

def verify_session_spotify():
    while True:
        obtener_hora_actual()
        mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
        maximizar_spotify()
        time.sleep(2.1)
        rotate_time = random.randint(12 * 60 * 60)
        time.sleep(rotate_time)
        if buscar_imagen_en_pantalla("spotify_is_playing_ok.png"):
            print(f"{mensaje_hora} spotify esta abierto, la cuenta esta OK...")                    
            minimizar_spotify() 
        else:
            print(f"{mensaje_hora} No se encontró la imagen, parece que spotify no esta corriendo o la sesion no esta abierta")
            taket_screenshot_send_telegram()
            print(f"{mensaje_hora} Se creará una nueva cuenta...")
            register_spotify_account()




fecha_creacion_str = fecha_creacion
def calcular_edad_cuenta():
    fecha_creacion = datetime.datetime.strptime(fecha_creacion_str, "%Y-%m-%d %H:%M:%S.%f")
    fecha_actual = datetime.datetime.now()
    diferencia = fecha_actual - fecha_creacion
    edad_dias = diferencia.days
    edad_horas = diferencia.seconds // 3600
    return edad_dias, edad_horas

edad_dias, edad_horas = calcular_edad_cuenta()


def verificacion_edad_cuenta():
    # Bucle para ejecutar las tareas programadas
    while True:
        edad_dias, edad_horas = calcular_edad_cuenta()
        print(f"Edad de la cuenta: {edad_dias} días y {edad_horas} horas")
        
        # Realizar la acción cuando la cuenta tenga 6 días y 12 horas de edad
        if edad_dias == 6 and edad_horas == 12:
            # Código para ejecutar la acción deseada
            print("La cuenta tiene 6 días y 12 horas de edad. se crera una nueva cuenta...")

        # Esperar 12 horas antes de la próxima verificación
        time.sleep(30)    # 12horas=12 * 60 * 60   

def main():
     
    #verificar_y_abrir_spotify()
    # Crear hilos para ejecutar las tareas
    hilo_edad_cuenta = threading.Thread(target=verificacion_edad_cuenta)
    #hilo_playlist = threading.Thread(target=play_playlists_continuosly)
    #hilo_verificar_playing = threading.Thread(target=verificar_playing, args=(4,))
    #hilo_verificar_conexion = threading.Thread(target=verificar_conexion)

    # Iniciar los hilos
    #hilo_edad_cuenta.start()
    #hilo_playlist.start()
    #hilo_verificar_playing.start()
    #hilo_verificar_conexion.start()

    # Esperar a que los hilos terminen (esto no sucederá porque las tareas se ejecutan en bucles infinitos)
    #hilo_edad_cuenta.join()
    #hilo_playlist.join()
    #hilo_verificar_playing.join()
    #hilo_verificar_conexion.join()

if __name__ == "__main__":
    main()