import calendar,string, random, time, requests, re, os,subprocess,pyautogui, configparser, datetime
from random import randint, choice, choices
from colorama import Fore, Style


pausa = random.uniform(1000, 2000) / 1000
pyautogui.PAUSE = pausa

def obtener_hora_actual():
    hora_actual = time.strftime("%H:%M:%S")
    return hora_actual
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"


# Funcion para generar un retardo aleatorio en milisegundos
def perform_task_with_delay():
    random.seed(time.time_ns()) 
    for _ in range(5):
        sleep_time = random.uniform(2000, 7000) / 1000
        time.sleep(sleep_time)


def getUsername() -> str:
    nick = list()
    prefix = str()
    under_score = str()
    under_score2 = str()
    rnd_number = str()
    rnd_vowels = choices(("a", "e", "i", "o", "u", "y"), k=randint(7, 9))
    rnd_consonant = choices(
        ("b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","y","z", ),
        k=randint(8, 16),
    )

    nick = [f"{x}{y}" for x, y in list(zip(rnd_vowels, rnd_consonant))]
    if choice((True, False)):
        if choice((True, False)):
            under_score = "_"

        prefix = choice(
            (
                "Mr","Ms","Sir", "Doctor","Lord","Lady","Rabbi","General","Captain","Glide","Deedee","Dazzle","Daydream","Micro","Lion","Punch","Hawk",
                "Sandy","Hound","Rusty","Tigress","Commando","Abbot","Invincible","SepuLtura","Detective","Vanguard","Storm","Soulfly","Marine",
                "Saber","Parachute","4Justice","StrongHold","Thunder","Discoverer","Explorer","Cardinal","Winner","Bee","Aranhita","Munchkin",
                "Teddy","Scout","Smarty","Dolly","Princesa","Pumpkin","Sunshine","Tinkerbell","Bestie","Sugar","Juliet","Magician","Mule","Stretch",
                "Missile","Alpha","Grace","el-loco","King","El-rey","Oldie","Poker","Bustier","Adonis","Squirt","Ace","Mortal","Speedy","Bug","Senior",
                "Bear","Rifle","Insomnia","JustWatch","Macunba","Creature","Miracle","SuperHero","WhoAmI","Handyman","TheTalent","Boss","Meow","Ms.Congeniality",
                "Rapunzel","Dolly","Sunshine","Eirene","Drum","Miracle","Cuban","Repartero","Chico-Malo","el-retro","electrico","elquemador","ladiablita","elzorro",
                "musiquera","lacaballota","lafiera","Supermusico","chico","chiquillamala","mariposa","elmadrugador","elreparador","laquetemata","justicia",
                "amador","justicia","PazyLibertad","LaExploradora","ElGeneral","ElSuper","AbejaMala","ElPidio","Matojo","elinvencible""enamorada","caliente",
                "MariaSilvia","ElLibertador","CR7Cubano","PrincessdeCuba","Habaner","LaGiraldilla","RonSantiago","Mulat","elChochero","laMakina","Almendron","ElBodeguero",
                "elfuerte","ElMatador","LaQueTegusta","LaQueTemata","ElComplice","LaReina","SuperFlow","Canela","LaRubiaMala","LaMascara","Patineta","LaCaballota",
                "LaInmortal","CriaturaSexy","ElLocoSoyYo","Romantico","Romantica","Balsero","Elcoyote","HeladoCoppelia","ElMecanico","TornadoEnCuba",
                "MunhecaCruel","MiracleCuba","ChicaPicante","TalentoUrbano","Mezclador","El-Jefe","Camarera","Aeromosa","ElGeneral","Palmiche","Guazo",
                "LaLimonada","Guarapo","Electrico","locota","caballota","perreo","callejero","mechador","chicanerd","lamachi","zorro_cu","elgato_cu","eloso",
            )
        )

    if choice((True, False)):
        if choice((True, False)):
            under_score2 = "_"
        rnd_number = f"{under_score2}{randint(1, 99)}"

    nick = prefix + under_score + "".join(nick).capitalize() + rnd_number
    return nick



def maximizar_spotify():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    result = subprocess.run(["xdotool", "search", "--class", "spotify"], capture_output=True, text=True)
    output = result.stdout.strip()
    spotify_ids = output.split()
    for spotify_id in spotify_ids:
        subprocess.run(["xdotool", "windowactivate", spotify_id])
        result = subprocess.run(["xdotool", "getwindowgeometry", spotify_id], capture_output=True, text=True)
        geometry_output = result.stdout.strip()
        if "Maximized" in geometry_output:
            break
    if not spotify_ids:
        print(f"{mensaje_hora} No se encontró la ventana de Spotify.")

def minimizar_spotify():
    result = subprocess.run(["xdotool", "search", "--class", "spotify"], capture_output=True, text=True)
    output = result.stdout.strip()
    spotify_ids = output.split()
    for spotify_id in spotify_ids:
        # Minimizar la ventana de Spotify
        subprocess.run(["xdotool", "windowminimize", spotify_id])
    if not spotify_ids:
        print(f"{mensaje_hora} No se encontró la ventana de Spotify.")


# Generar un Password para la Cuenta
def Generate_Password_Account_Spotify():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    # Generate a new random password
    password_length = random.randint(12, 16)
    digits = random.choices(string.digits, k=2)
    characters = random.choices(
        string.ascii_lowercase + string.ascii_uppercase + string.digits,
        k=password_length - 2,
    )
    new_password = "".join(digits + characters)
    print(f"{mensaje_hora} Generando una Nueva Clave.")
    return new_password


def lanzar_spotify():
    try:
        subprocess.Popen(['/usr/bin/spotify', '%U', '--no-zygote', '--disable-gpu', '--disable-software-rasterize'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(4.1)
        print(f"{mensaje_hora}  Abriendo Spotify App.")
        subprocess.Popen(['sp', 'play'])   
        return True
    except FileNotFoundError:
        print(f"{mensaje_hora}  Spotify no se encuentra instalado en el sistema.")
        return False

# Teclear texto en Formularios usando XdoTool
def type_text(text):
    try:
        subprocess.run(['xdotool', 'type', text], check=True)
    except subprocess.CalledProcessError:
        print("Error occurred while typing text.")



def establish_vpn_connection(vpn_name):
    try:
        subprocess.run(["sudo","nmcli", "c", "up", vpn_name, "passwd-file", "/etc/NetworkManager/passwd-file"], check=True)
        print(f"{mensaje_hora} Established connection to {vpn_name}")
    except Exception as e:
        print(f"{mensaje_hora} Failed to establish connection to {vpn_name}: {str(e)}")
    

def disconnect_vpn(vpn_name):
    try:
        subprocess.run(["sudo","nmcli", "c", "down", vpn_name], check=True)
        print(f"{mensaje_hora} Disconnected from {vpn_name}")
    except Exception as e:
        print(f"{mensaje_hora} Failed to disconnect from {vpn_name}: {str(e)}")
    

def get_active_vpn():
    output = subprocess.check_output("nmcli c show --active | sed -n '/vpn/I s/\\s.*$//p'", shell=True).decode().strip()
    return output if output else None


def get_all_vpns():
    output = subprocess.check_output("nmcli c show | sed -n '/vpn/I s/\\s.*$//p'", shell=True).decode().strip().split('\n')
    return output if output else []
    

def connect_vpn_randomly():
    active_vpn = get_active_vpn()
    all_vpns = get_all_vpns()
    #if active_vpn:
       # disconnect_vpn(active_vpn)
    if all_vpns:
        random_vpn = random.choice(all_vpns)
        establish_vpn_connection(random_vpn)
        

# cerrar  todas las ventanas 
def close_all_windows():
    command = "wmctrl -l | grep -v ' -1 ' | awk '{print $1}' | xargs -I {} wmctrl -ic {}"
    try:
        subprocess.run(command, shell=True, check=True)
        print("{mensaje_hora}  All windows closed.")
    except subprocess.CalledProcessError as e:
        print(f"{mensaje_hora} Error executing the command: {e}")

def read_config():
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))    
    # Read 'Credentials'
    your_username = config.get('Credentials', 'Username')
    your_password = config.get('Credentials', 'Password')
    creation_date = config.get('Credentials', 'creation_date')
    virtual_machine = config.get('Play_Lists', 'virtual_machine')
    # Telegram bot chat id
    bot_token = config.get('telegram_bot', 'token')
    bot_chat_ids = config.get('telegram_bot', 'chat_ids')
    # id de acceso a la api de spotify
    client_id = config.get('spotify_credentials', 'client_id')
    client_secret = config.get('spotify_credentials', 'client_secret')     
    return your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, client_id, client_secret


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

# Leer todas las configuraciones
# para leer independiente: ejemplo duration = read_config()[4]
your_username, your_password,creation_date,virtual_machine,bot_token,bot_chat_ids, client_id, client_secret = read_config()
playlist_id = obtener_ids_playlist()

# Obtener la ruta absoluta del directorio del script
script_directory = os.path.dirname(os.path.abspath(__file__))

def buscar_imagen_y_clic(image_path, num_intentos=15, timeout=30, **kwargs):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    start_time = time.time()
    ruta_completa = os.path.join(script_directory, 'images', image_path)  # Ruta completa de la imagen
    for i in range(num_intentos):
        match = pyautogui.locateOnScreen(ruta_completa, **kwargs)
        if match:
            # La imagen se encontró, hacer clic en ella
            image_location = pyautogui.center(match)
            pyautogui.click(image_location)
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

def click_images(images, timeout=30, interval=1, delay=1):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    start_time = time.time()
    found_images = []  # Lista para almacenar las imágenes encontradas

    script_directory = os.path.dirname(os.path.abspath(__file__))
    images_directory = os.path.join(script_directory, 'images')

    while time.time() - start_time < timeout:
        for image_path in images:
            ruta_completa = os.path.join(images_directory, image_path)  # Ruta completa de la imagen
            location = pyautogui.locateOnScreen(ruta_completa)
            if location is not None:
                # Imagen encontrada, realizar acción de clic
                image_center_x, image_center_y = pyautogui.center(location)
                pyautogui.click(image_center_x, image_center_y)
                print(f"{mensaje_hora} Encontrada la imagen {image_path} en captura, haciendo clic...")
                found_images.append(image_path)  # Agregar la imagen encontrada a la lista
                time.sleep(delay)  # Insertar el retraso o tiempo de espera después de cada clic

        if found_images:
            print(f"{mensaje_hora} Encontradas las imagenes {found_images} ...")
            return found_images  # Retornar la lista de imágenes encontradas

        time.sleep(interval)
    
    return found_images  # Retornar la lista de imágenes encontradas (puede estar vacía)


new_email = getUsername() + ('@yopmail.com')
new_name = getUsername()

tipeslow = random.uniform(500, 1000) / 1000

# Crear y llenar el Formulario para crear la cuenta de Spotify
def llenar_formulario_crear_spotify_cuenta():
    password = Generate_Password_Account_Spotify()
    tipeslow = random.uniform(500, 1000) / 1000
    lista_imagenes_genero = [     # Lista de Imagenes correspondientes a los Géneros
        'register_account_Man.png',
        'register_account_woman.png',
        'register_account_no_say.png',
        'register_account_non_binary.png',
        'register_account_else.png'
    ]
    imagen_genero_aleatorio = random.choice(lista_imagenes_genero)    # Seleccionar una imagen aleatoria
    # Crear la Cuenta insertar los datos
    pyautogui.typewrite(new_email,interval=0.2)
    pyautogui.press('enter')      
    if buscar_imagen_y_clic('register_account_next.png'):
        print(f"{mensaje_hora} Insertando cuenta de Correo {new_email} y click siguiente")

        if buscar_imagen_y_clic('register_account_2.png'):
            print(f"{mensaje_hora} Insertando password {password} y click siguiente")
            pyautogui.typewrite(password,interval=0.2)
            buscar_imagen_y_clic('register_account_next_1.png')
            print(f"{mensaje_hora} Click siguiente")

            if buscar_imagen_y_clic('register_account_Name.png'):
                pyautogui.typewrite(new_name,interval=tipeslow)
                print(f"{mensaje_hora} Insertando Nombre {new_name} ")
                pyautogui.press('tab')
                time.sleep(tipeslow)
                pyautogui.press('tab')
                # Entrar Mes
                # Genera un número aleatorio entre 1 y 12
                random_month = random.randint(1, 12)
                # Presiona la tecla de flecha abajo el número de veces aleatorio
                for _ in range(random_month):
                    pyautogui.press('down')
                pyautogui.press('tab')
                print(f"{mensaje_hora} Insertando Mes ")
                # Entrar Dia
                random_day = random.randint(1, 28)
                pyautogui.typewrite(str(random_day),interval=tipeslow)
                print(f"{mensaje_hora} Insertando Dia  ")
                pyautogui.press('tab')
                # Entrar el Año
                year = (random.randint(1989, 2003))
                pyautogui.typewrite(str(year),interval=tipeslow)
                print(f"{mensaje_hora} Insertando año ")
                # Genero    
                # Llamar a la función con la imagen seleccionada de forma aleatoria
                time.sleep(tipeslow)
                buscar_imagen_y_clic(imagen_genero_aleatorio)
                print(f"{mensaje_hora} Seleccionando Genero aleatorio ")
                time.sleep(tipeslow)
                if buscar_imagen_y_clic('register_account_next_1.png', grayscale=True, confidence=0.8):
                    print(f"{mensaje_hora} Click Siguiente ")
                    if buscar_imagen_y_clic('register_account_SignUp.png', grayscale=True, confidence=0.8):
                        print(f"{mensaje_hora} Click Botón SignUp ")
                    else:
                        print(f"{mensaje_hora} No se encontró el botón de SignUp, accediento con TAB y ENTER ")
                        pyautogui.press('tab')
                        pyautogui.press('enter')
                else:
                    print(f"{mensaje_hora} No se encontró el botón de Siguiente, accediento con TAB y ENTER ")
                    pyautogui.press('tab')
                    pyautogui.press('enter')
            else:
                print(f"{mensaje_hora} No se Encontró el campo de formulario del Nombre")
        else:
            print(f"{mensaje_hora} No se Encontró el campo de formulario del password")
    else:
        print(f"{mensaje_hora} No se Encontró el botón Next presionando enter")
        pyautogui.press('enter')
    print(f"{mensaje_hora} Se completo el formulario y enviarlo para Crear la cuenta")
    print(f"{mensaje_hora} Cuenta {new_name} con Email: {new_email} Clave: {password} fue creada y Guardada...")
    #write_credentials(new_email, password)       # Salvar las credenciales creadas al fichero
    #update_config(new_password=password, new_username=new_email)
    fecha_creacion = datetime.datetime.now()
    update_config(new_username=str(new_email), new_password=str(password),fecha_creacion=fecha_creacion)
    # SAve Data to File
    time.sleep(5.0)


def close_firefox_window():
    print(f"{mensaje_hora} Cerrando FireFox.")
    subprocess.run(['xdotool', 'search', '--onlyvisible', '--name', 'Mozilla Firefox', 'windowactivate', '%1'])
    time.sleep(1.5)
    subprocess.run(['xdotool', 'key', 'Alt+F4'])


# Función para seguir las istas de eproduccion
def seguir_lista_profile(perfil_spotify, imagen_seguir, *args, **kwargs):
    subprocess.run(['sp', 'open', perfil_spotify])
    # Esperar unos segundos para que cargue completamente
    time.sleep(4.1)
    # Buscar la imagen p}ara seguir al artista
    resultado, coordenadas = buscar_imagen_y_clic(imagen_seguir, **kwargs)
    if resultado:
        print(f"{mensaje_hora} Se siguió al artista:", perfil_spotify)
    else:
        print(f"{mensaje_hora} No se pudo seguir al artista:", perfil_spotify)
    # Hacer una pausa después de seguir al artista
    time.sleep(2.1)




def update_config(new_password=None, new_username=None, fecha_creacion=None,new_virtual_machine=None, new_playlists=None):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    print(f"{mensaje_hora} Actualizando la información en el archivo de configuración")
    config = configparser.ConfigParser()
    file_path = os.path.join(os.path.dirname(__file__), "account.txt")
    config.read(file_path)
    
    if new_password:
        config.set('Credentials', 'password', str(new_password))
    if new_username:
        config.set('Credentials', 'username', str(new_username))
    if fecha_creacion:
        config.set('Credentials', 'fecha_creacion', str(fecha_creacion))        
    if new_virtual_machine:
        config.set('Credentials', 'virtual_machine', str(new_virtual_machine))
    if new_playlists:
        for i, playlist in enumerate(new_playlists, start=1):
            section_name = f'Playlist{i}'
            config.set(section_name, 'id', playlist[0])
            config.set(section_name, 'nombre', playlist[1])
            config.set(section_name, 'duracion', playlist[2])

    with open(file_path, 'w') as config_file:
        config.write(config_file)


from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

#    Obtener info de la playlist online via spotipy
def obtener_info_playlist(playlist_id):
    # Configurar las credenciales del cliente de Spotify
    client_id = 'ee204ef35a9f4ae3affce9400fda2c2a'
    client_secret = '46696c68f11f4a85807f6c030a6598e7'    
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)
    # Obtener los detalles de la playlist utilizando su ID
    playlist = sp.playlist(playlist_id)
    total_duration_ms = 0
    for track in playlist['tracks']['items']:
        track_info = track['track']
        if track_info is not None:  # Verificar que track_info no sea None
            total_duration_ms += track_info['duration_ms']

    playlist_duration_minutes = (total_duration_ms // 1000 // 60) + 1
    playlist_name = playlist['name']
    playlist_url = playlist['external_urls']['spotify']
    playlist_cover_image = playlist['images'][0]['url']
    return {
        'nombre': playlist_name,
        'duracion': playlist_duration_minutes,
        'url': playlist_url,
        'imagen_portada': playlist_cover_image,
    }


def iniciar_sesion_real_spotify():
    # Leer La info del fichero de texto que almacena el correo y la clave
    # Funcion para iniciar sesion real simulando Ser Humano con PyAutoGUI
    # Desconectar Conexiones VPN
    #active_vpn = get_active_vpn()
    #if active_vpn:
    #    disconnect_vpn(active_vpn)
    lanzar_spotify()
    time.sleep(3.1)
    # Paso 2: Verificar si la sesión ya está iniciada chequeando la imagen de inicio.
    # Si no encuentra la imagen es que ya la sesion esta abierta y termina.
    max_attempts = 10
    Spotify_Session_Login_Screen = None
    attempt = 0
    while Spotify_Session_Login_Screen is None and attempt < max_attempts:
        Spotify_Session_Login_Screen = pyautogui.locateCenterOnScreen('1_Spotify_Login_Button.png')
        attempt += 1
        time.sleep(1.1)
    if not Spotify_Session_Login_Screen:
        print(f"{mensaje_hora} La sesión parece esta iniciada saliendo y ejecutando monitoreo de Spotify...")
        exit()
    else:
        print(f"{mensaje_hora} Se Detectó el Welcome Screen de Spotify se iniciará la sesion Real like human...")
        # Clic en el boton del spotify para iniciar sesion y se abra el navegador
        # if not pyautogui.locateOnScreen('Spotify_Session_Login_Screen.png'):
        #    print(f"{mensaje_hora} La sesion esta iniciada saliendo y ejecutando monitoreo de Spotify")
        #    exit()
        # Paso 3: Iniciar sesión
        # Clic en el boton de iniciar sesion
        if buscar_imagen_y_clic('1_Spotify_Login_Button.png'):
            # Paso 4: Se Abre el navegador el navegador
            time.sleep(8.5)
            # Paso 5:  buscar campo de formulario e Iniciar sesión dentro del navegador
            if buscar_imagen_y_clic('2_Email_Username.png'):
                # Aquí debes agregar el código para insertar el usuario y la clave utilizando pyautogui
                print(f"{mensaje_hora} Se encontró el login en la pagina, haciendo click para llenar el formulario")
                time.sleep(3.2)
                pyautogui.hotkey('ctrl','a')
                pyautogui.press('delete') # eliminando Entradas.  
                # Retrieve a single set of username and password.
                pyautogui.typewrite(your_username)
                pyautogui.press('tab')
                pyautogui.typewrite(your_password)
                pyautogui.press('enter')  # Press Enter to login.
                print(f"{mensaje_hora} Se completo el formulario y enviarlo para iniciar sesión")
                time.sleep(8.5)
                # Paso 6: Click en el Boton Continuar con la aplicación.
                if buscar_imagen_y_clic('3_Image_Continue_APP.png', grayscale=True, confidence=0.8):
                    # La secuencia de pasos se completó con éxito
                    print(f"{mensaje_hora} formurario completado, iniciando sesion")
                    time.sleep(15.1)
                    close_firefox_window()
                else:
                    print(f"{mensaje_hora} No se encontró la imagen para continuar con la aplicación, Bajando con TAB.")
                    time.sleep(pausa)
                    subprocess.run(['xdotool', 'key', 'Tab']) # bajar al boton con tab
                    print(f"{mensaje_hora} Bajar al Login con Tab key")
                    type_text(your_username)
                    subprocess.run(['xdotool', 'key', 'Tab'])    
                    type_text(your_password)    # Type password
                    subprocess.run(['xdotool', 'key', 'Return']) # Press enter
            else:
                print(f"{mensaje_hora} No se encontró la imagen del login para el sesión dentro del navegador.")
        else:
            print(f"{mensaje_hora} No se encontró la imagen de inicio de sesión de la APP Spotify")
    subprocess.run(['sp', 'play'])
    
# Crear nueva Cuenta de Spotify usando pyautogui simulando ser humano
def register_spotify_account():
    #active_vpn = get_active_vpn()
    #if active_vpn:
    #    disconnect_vpn(active_vpn)    
    lanzar_spotify()   
    time.sleep(6.5)
    print(f"{mensaje_hora} Se va a Crear una Nueva Cuenta")
    # Paso 2: Buscar la imagen del  Registrar la Cuenta o Crear cuenta en Spotify
    if buscar_imagen_y_clic("1_Sign_Up_Free.png"):
        # Esperar que Abra Firefox para llenar el Formulario de crear la Cuenta
        time.sleep(8.5)
        if buscar_imagen_y_clic('register_account_0.png', grayscale=True, confidence=0.8):
            # Crear la cuenta Llenar el Formulario en Firefox
            # Llenar el formulario con los datos disponibles
            llenar_formulario_crear_spotify_cuenta()
            time.sleep(8.5)
            # Paso adicional: Hacer clic en el botón "No soy un robot" (primero)
            if buscar_imagen_y_clic('not_machine_1.png'):
                time.sleep(1.5)  # Esperar a que se complete la verificación
                if buscar_imagen_y_clic('not_machine_2.png'):
                    time.sleep(1.1)  # Esperar a que se complete la verificación
                    if buscar_imagen_y_clic('not_machine_3.png'):
                        time.sleep(1.1) 
                        if buscar_imagen_y_clic('3_Image_Continue_APP.png', grayscale=True, confidence=0.8):
                            print(f"{mensaje_hora} haciendo clic en Continuar para abrir Spotify")
                            time.sleep(15.1)
                        else:
                            print(f"{mensaje_hora} No se encontró botón para continuar, Bajar con TAB")
                            pyautogui.press('tab')
                            pyautogui.press('enter')   
                else:
                    print(f"{mensaje_hora} No se encontró el botón 'No soy un robot - 1'")
            else:
                print(f"{mensaje_hora} No se encontró el botón 'No soy un robot - 2'")       
        else:
            print(f"{mensaje_hora} No se encontró el Campo del formulario para crear la Cuenta")
    else:
        print(f"{mensaje_hora} No se encontró el boton para clickear y comenzar a crear la cuenta")
    time.sleep(8.5)
    seguir_lista_profile('spotify:playlist:{}'.format(playlist_id), 'follow_pl_music_fresh.png', grayscale=True, confidence=0.6)        
    #init_account_spotify()

def seguir_artist_list_aleatorias():    # Funcion para realizar el seguimiento de los diferentes profiles de forma aleatorias
 
    def seguir_Tia_yamilet_PL():
        seguir_lista_profile('spotify:playlist:{}'.format(playlist_id), 'follow_pl_music_fresh.png', grayscale=True, confidence=0.6)        
        #seguir_lista_profile('spotify:playlist:1HuHGRuzS11lEedvR8TfsX', 'Tia_Yamilet_PL.png', grayscale=True, confidence=0.6)

    def seguir_yandys_alfonso86():
        seguir_lista_profile('spotify:user:yandys.alfonso86', 'follow_yandys_profile.png')

    def seguir_RepartoMisucLMB():
        seguir_lista_profile('spotify:playlist:4So3pJ7GCBPsL7UQL0ZTpy', 'Like_RepartoMisucLMB.png', grayscale=True, confidence=0.6)

    def seguir_PlayLisReparteros():
        seguir_lista_profile('spotify:playlist:0WzFRK2BckCJwBtGdMPV5n', 'Like_PlayLisReparteros.png', grayscale=True, confidence=0.6)

    def seguir_Tia_yamilet_profile():
        seguir_lista_profile('spotify:user:zipousrwyhzkiuv10vph1r5iu', 'kuki-channel-profile.png', grayscale=True, confidence=0.6)

    sentencias = [seguir_Tia_yamilet_PL]
    random.shuffle(sentencias)

    for sentencia in sentencias:
        sentencia()

def init_account_spotify():
    #despues de creada la Cuenta se realizaran acciones 
    # para seguir las listas y profiles especificos
    time.sleep(5.1)
    time.sleep(pausa)
    maximizar_spotify()
    time.sleep(6.1)
    time.sleep(pausa)
    image_paths = ['Spotify_Dismiss_1.png',      # Si aparece el cartel ese de Aceptar cerrarlo
                   'Spotify_Dismiss_2.png',    # Si aparece el cartel ese de Aceptar cerrarlo
                   'Spotify_Dismiss_3.png',    # Si aparece el cartel ese de Aceptar cerrarlo
                   'Spotify_Dismiss_4.png',    # Si aparece el cartel ese de Aceptar cerrarlo
                   #'Click_Random.png',      # Clic en el boton de Aleatorio 
                   'Click_Repeat.png',       # Clic en el Boton de Repetir la Play List
                   'Click_Like.png']       # Clic en el Like a la cancion que este actual
    time.sleep(8.1)               
    result = click_images(image_paths, timeout=20, interval=2, delay=1)
    if result:
        print(f"{mensaje_hora} Image found and clicked!")
    else:
        print(f"{mensaje_hora} Image not found within the timeout.")
    time.sleep(6.1)
    minimizar_spotify()