import time,subprocess,random, re
from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual,maximizar_spotify, buscar_imagen_y_clic, click_images, seguir_lista_profile, minimizar_spotify 

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"


    
def seguir_artistas():
    maximizar_spotify()
    buscar_imagen_y_clic('/home/lmb/spotify/images/Click_Like.png')
    # Extraer la cadena  URI del Artista
    def extraer_cadena_url(url):
        patron = r'\/artist\/(.*?)\?'
        resultado = re.search(patron, url)
        if resultado:
            return resultado.group(1)
        else:
            return None
    # Ruta al archivo que contiene las URLs
    archivo_entrada = "/home/lmb/Spotify-Script/Artistas.txt"
    # Leer las URLs del archivo
    with open(archivo_entrada, "r") as archivo:
        lineas = archivo.readlines()
    # Elegir una URL aleatoriamente
    url_elegida = random.choice(lineas).strip()
    # Extraer la cadena de la URL
    cadena_extraida = extraer_cadena_url(url_elegida)
    if cadena_extraida:
        # Formar la cadena deseada
        cadena_formada = f'spotify:artist:{cadena_extraida}'
        #subprocess.run(cadena_formada.split())
        time.sleep(3.3)
        image_paths = ['/home/lmb/spotify/images/Spotify_Dismiss_1.png',
                       '/home/lmb/spotify/images/Spotify_Dismiss_2.png',]
        time.sleep(8.7)               
        result = click_images(image_paths, timeout=15, interval=2, delay=1)
        seguir_lista_profile(cadena_formada, '/home/lmb/spotify/images/follow_artist.png', grayscale=True, confidence=0.6)
    else:
        print(f"{mensaje_hora} No se encontró la cadena entre '/' y '?' en la URL.")    
    time.sleep(3.3)
    buscar_imagen_y_clic('/home/lmb/spotify/images/Click_Like.png')
    print(f"{mensaje_hora} Clic Cancion ")
    subprocess.run(['sp', 'open', 'spotify:playlist:1HuHGRuzS11lEedvR8TfsX'])
    minimizar_spotify()


time_to_change = random.randint(1000, 5000)
retardo_segundos = time_to_change / 1000
time.sleep(retardo_segundos)
seguir_artistas()

