from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import random, time, datetime, os,asyncio,configparser,sys
from colorama import Fore, Style
from telegram import Bot
from function_utils_aux import obtener_hora_actual,read_config
from telegram_aux import enviar_archivo_telegram

if len(sys.argv) == 4:
    playlist_id = sys.argv[1]
    nombre_playlist = str(sys.argv[2])
    playlist_duration = str(sys.argv[3])
else:
    your_username, your_password,creation_date,playlist_id,virtual_machine,bot_token,bot_chat_ids, spotify_client_id, spotify_client_secret = read_config()
    bot_chat_ids = bot_chat_ids.split(',')  # split string to read multiples vaues separated by ,

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
DIRECTORY = os.path.join(os.path.dirname(__file__), "Stats")
now = datetime.datetime.now() 
timestamp = now.strftime("%d-%m-%Y_%H-%M")
filename = "{}_{}.png".format(playlist_id, timestamp)
nombre_archivo = (os.path.join(DIRECTORY, filename))


def iniciar_sesion_get_stats(url, username, password):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    print(f"{mensaje_hora} Iniciando sesion en modo marioneta con la cuenta {your_username}")
    firefox_options = Options()
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
    ]
    random_user_agent = random.choice(user_agents)

    firefox_options = Options()
    random_user_agent = random.choice(user_agents)
    firefox_options.set_preference("general.useragent.override", random_user_agent)
    print(f'{mensaje_hora} User Agent: {random_user_agent}')
    browser = webdriver.Firefox(options=firefox_options)
    browser.get(url) 
    time.sleep(3.1)
    browser.find_element(By.XPATH, "//input[@id='login-username']").send_keys(username)
    browser.find_element(By.XPATH, "//input[@id='login-password']").send_keys(password)
    browser.find_element(By.ID, 'login-button').click()
    print(f"{mensaje_hora} Insertando Usuario {username} y Clave {password} para iniciar sesion")
    wait = WebDriverWait(browser, 15) 
    error_message = "//span[contains(.,'Oops! Something went wrong, please try again or check out our help area')]"
    try:
        error_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, error_message)))
        print(f"{mensaje_hora} Se encontro error reintentando")
        browser.find_element(By.ID, 'login-button').click()
        print(f"{mensaje_hora} Se hizo clic en el botón nuevamente")
        browser.find_element(By.XPATH, "//p[contains(.,'Agree')]").click()
    except:
        try:
            success_element =  WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(.,'Agree')]")))
            print(f"{mensaje_hora} El Error no está presente en la página por tanto todo  esta bien")   
            #wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='root']/div/div[2]/div/div/div[3]/button/span")))
            browser.find_element(By.XPATH, "//p[contains(.,'Agree')]").click()

        except:
            time.sleep(15.1)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(.,'Recently played Tracks')]")))
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            print(f'{mensaje_hora} Esperando que cargue la pagina completamente')

    time.sleep(25.1)
    browser.save_full_page_screenshot(nombre_archivo)
    print(f'{mensaje_hora} Salvando página web como {nombre_archivo} y esperando unos segundos')
    time.sleep(10.1)
    browser.quit()
    print(f'{mensaje_hora} Cerando Navegador')
    print(f"{mensaje_hora} La página web se ha guardado como {filename} en el directorio {DIRECTORY}")    

    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    archivo_configuracion = os.path.join(directorio_actual, "playlists", playlist_id + ".ini")

    config = configparser.ConfigParser()
    config.read(archivo_configuracion)
    # Leer los campos de la sección 'Playlist'
    playlist_name = config.get('Playlist', 'nombre')
    playlist_duration_minutes = int(config.get('Playlist', 'duracion'))
    playlist_url = config.get('Playlist', 'url')
    playlist_cover_image = config.get('Playlist', 'imagen_portada')
    caption_mensaje = (f'{playlist_name}\nDuración:{playlist_duration_minutes}\nURL:\n{playlist_url}\nPortada:\n{playlist_cover_image}')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(enviar_archivo_telegram(bot_token, bot_chat_ids, archivo=nombre_archivo, caption=caption_mensaje))


def main():
    import subprocess

    url = "https://www.statsforspotify.com/track/recent"
    iniciar_sesion_get_stats(url, your_username, your_password)
    time.sleep(10)
    #os.remove(nombre_archivo)

if __name__ == "__main__":
    main()