from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import random, time, os, pyautogui,sys,asyncio, datetime
from function_utils_aux import * 
from selenium.common.exceptions import TimeoutException
from function_utils_aux import obtener_hora_actual,connect_vpn_randomly,disconnect_vpn,get_active_vpn,read_config
from telegram_aux import enviar_archivo_telegram
# Script para iniciar sesion en spotify en modo Marionette, 
# si la sesion falla intentará cambiar la clave. Si en el 
# proceso el mensaje de correo no llega al buzón con el 
# enlace se deberá crear una nueva cuenta de usurio.

os.environ['DISPLAY'] = ':0'
# Desconectar VPN  antes de iniciar sesion
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36",
    "Mozilla/5.0 (Android 10; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    # Add more User-Agent strings as needed
]
active_vpn = get_active_vpn()
if active_vpn:
    disconnect_vpn(active_vpn)

#subprocess.run(['pkill', 'spotify'])
#print(f"{mensaje_hora} Cerrando cualquier instancia de Spotify que exista abierta")

# Choose a random User-Agent from the list
random_user_agent = random.choice(user_agents)

# Continue with other actions using the browse
firefox_options = Options()
# Choose a random User-Agent from the list
random_user_agent = random.choice(user_agents)
firefox_options.set_preference("general.useragent.override", random_user_agent)
print(f'{mensaje_hora} User Agent: {random_user_agent}')

# Set up Firefox options
browser = webdriver.Firefox(options=firefox_options)

# Verificar si se pasaron los argumentos enecesarios y si no leerlo desde archivo.
if len(sys.argv) == 4:
    # Cargar los argumentos como variables
    playlist_id = sys.argv[1]
    nombre_playlist = str(sys.argv[2])
    playlist_duration = str(sys.argv[3])
else:
    # Cargar las variables desde el archivo
    your_username, your_password, playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()


mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"


# Directorio para guardar las imágenes
DIRECTORY = os.path.join(os.path.dirname(__file__), "Stats")  # Ruta al directorio donde se guardará la imagen
# Token de acceso del bot de Telegram
token = "6563344306:AAEXTdxkC1btSc-C2nV3cfts6r5ZSy_ABGw"
chat_ids = ["699683569","828562504"]       # ID del Chat
#caption = description  # Descripción o leyenda que deseas enviar
now = datetime.datetime.now()    # Obtener la fecha y hora actual
timestamp = now.strftime("%d-%m-%Y_%H-%M")
#   normalized_filename = re.sub(r'[^\w\-_.]', '', nombre_playlist)
filename = "{}_{}.png".format(playlist_id, timestamp)
nombre_archivo = (os.path.join(DIRECTORY, filename))

# Navegar a la página de inicio de sesión
browser.get(url="https://www.statsforspotify.com/track/recent")


def iniciar_sesion(browser):
    ## Leer Credenciales
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.txt"))
    your_username = config['Credentials']['username']
    your_password = config['Credentials']['password']
    # Localizar y completar los campos de usuario y contraseña
    browser.find_element(By.XPATH, "//input[@id='login-username']").send_keys(your_username)
    browser.find_element(By.XPATH, "//input[@id='login-password']").send_keys(your_password)
    browser.find_element(By.ID, 'login-button').click()


def verify_incorrect_username_password(browser):
    error_message = "//span[contains(.,'Incorrect username or password.')]"
    try:
        # Verificar si se muestra el mensaje de error
        error_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, error_message)))
        print(f'{mensaje_hora} usuario o contraseña incorrecto') 
        return True
    except:
        print(f'{mensaje_hora} Se inicio correctamente la sesion') 
        return False
    
def verify_something_went_wrong(browser):
    error_message = "//span[contains(.,'Oops! Something went wrong, please try again or check out our help area')]"
    try:     
        error_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, error_message)))
        print(f'{mensaje_hora} Algo salio mal en el inicio de sesion')         
        return True
    except:
        return False    

        
slow = random.uniform(500, 1000) / 1000


def get_stats(browser):
    # Verificar si se muestra el mensaje de error
    
    success_element = "//h2[contains(.,'Recently played Tracks')]"   
    try:
        error_element = wait.until(EC.visibility_of_element_located((By.XPATH, success_element)))
        wait = WebDriverWait(browser, 35)
        #browser.get(url="https://www.statsforspotify.com/track/recent")
        # Ingresa el correo en el campo de entrada
        time.sleep(5.1)
        time.sleep(35.1)
        browser.save_full_page_screenshot(nombre_archivo)
        print(f'{mensaje_hora} Salvando página web como {nombre_archivo} y esperando unos segundos')
        time.sleep(10.1)
        browser.quit()
        print(f'{mensaje_hora} Cerando Navegador')
        print(f"{mensaje_hora} La página web se ha guardado como {filename} en el directorio {DIRECTORY}")  
    except TimeoutException:
        # El elemento no existe o no es visible
        print("El elemento no existe o no es visible")
        time.sleep(4.1)
        return None
    finally:
        time.sleep(4.1)
        browser.quit()


# Actualizar la Clave en el Fichero
def send_capture_telegram(): 
    config = configparser.ConfigParser().read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "playlists", playlist_id + ".ini"))
    # Leer los campos de la sección 'Playlist'
    playlist_name = config.get('Playlist', 'nombre')
    playlist_duration_minutes = int(config.get('Playlist', 'duracion'))
    playlist_url = config.get('Playlist', 'url')
    playlist_cover_image = config.get('Playlist', 'imagen_portada')
    caption_mensaje = (f'{playlist_name}\nDuración:{playlist_duration_minutes}\nURL:\n{playlist_url}\nPortada:\n{playlist_cover_image}')
    loop = asyncio.get_event_loop()
    #   Enviando Mensaje con datos de la playlist
    #loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, mensaje=caption_mensaje))
    #   Enviando Foto adjunta con caption mensaje
    loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=nombre_archivo, caption=caption_mensaje))
    #   Enviando Archivo que contiene tracks y la informaciond e la lista
    # loop.run_until_complete(enviar_archivo_telegram(token, chat_ids, archivo=archivo_configuracion, caption=caption_mensaje))

    
iniciar_sesion(browser)

if verify_incorrect_username_password(browser):
 
    print(f"{mensaje_hora} Llamando funcion de cambio de clave")

elif verify_something_went_wrong(browser):
    print(f"{mensaje_hora} Reintentando")
    browser.find_element(By.ID, 'login-button').click()

get_stats(browser)
send_capture_telegram()

# Cerrar el navegador
browser.quit()