from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
#from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import random, time, os, pyautogui
from function_utils_aux import * 
from selenium.common.exceptions import TimeoutException

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

subprocess.run(['pkill', 'spotify'])
print(f"{mensaje_hora} Cerrando cualquier instancia de Spotify que exista abierta")

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

# Navegar a la página de inicio de sesión
browser.get(url="https://accounts.spotify.com/en/login")


def iniciar_sesion(browser):
    # Localizar y completar los campos de usuario y contraseña
    browser.find_element(By.XPATH, "//input[@id='login-username']").send_keys(your_username)
    browser.find_element(By.XPATH, "//input[@id='login-password']").send_keys(your_password)
    browser.find_element(By.ID, 'login-button').click()


def verificar_inicio_sesion_exitoso(browser):
    success_message = "//h2[contains(.,'Logged in as')]"
    try:
        # Verificar si se muestra el mensaje de éxito
        success_element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, success_message)))
        return True
    except:
        return False

def verificar_inicio_sesion_fallido(browser):
    error_message = "//span[contains(.,'Incorrect username or password.')]"
    try:
        # Verificar si se muestra el mensaje de error
        error_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, error_message)))
        return True
    except:
        return False
    
def verificar_inicio_sesion_fallido_1(browser):
    error_message = "//span[contains(.,'Oops! Something went wrong, please try again or check out our help area')]"
    try:
        # Verificar si se muestra el mensaje de error
        error_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, error_message)))
        return True
    except:
        return False    

def verificar_enlce_cambio_clave(browser):
    frame = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'ifmail')))
    browser.switch_to.frame(frame)
    link_password_change = "//a[contains(.,'Reset password')]"
    try:
        # Verificar si se muestra el mensaje de error
        link_element = WebDriverWait(browser, 5.1).until(EC.visibility_of_element_located((By.XPATH, link_password_change)))
        return True
    except:
        return False
        
slow = random.uniform(500, 1000) / 1000

new_password = Generate_Password_Account_Spotify()
confirm_password = new_password  # Use the same password for confirmation


def get_link_pwd_change(browser):
    browser = webdriver.Edge()
    try:
        browser.get(url="https://yopmail.com")
        # Ingresa el correo en el campo de entrada
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ycptcpt']/div[2]/div/input"))).send_keys(your_username)
        browser.execute_script("alert('Completa el CAPTCHA Manualmente! y Presiona ENTER en la CONSOLA al Terminar');")
        input("Presiona ENTER cuando hayas completado el captcha...")
        # Esperar hasta que el iframe esté presente y cambiar al iframe
        frame = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'ifmail')))
        browser.switch_to.frame(frame)
        time.sleep(2.1)
        reset_password_link = browser.find_element(By.XPATH, "//a[contains(.,'Reset password')]")
        reset_password_href = reset_password_link.get_attribute('href')
        return reset_password_href
    except TimeoutException:
        # El elemento no existe o no es visible
        print("El elemento no existe o no es visible")
        time.sleep(4.1)
        return None
    finally:
        time.sleep(4.1)
        browser.quit()


# Actualizar la Clave en el Fichero
def update_credentials(new_password): 
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.txt"))
    # Actualiza solo la clave 'Password' en la sección 'Credentials'
    config.set('Credentials', 'Password', new_password)
    with open('account.txt', 'w') as config_file:
        config.write(config_file)  # Guarda los cambios en el archivo de configuración

# Teclear y repetir el password usando pyautogui con Interaccion Real
def enter_repeat_passwd():
    move_mouse_click(150,150)
    time.sleep(5.1)
    pyautogui.press('tab',interval=tipeslow)
    pyautogui.typewrite(new_new_password_1,interval=tipeslow)
    pyautogui.press('tab',interval=tipeslow)
    pyautogui.typewrite(new_new_password_2,interval=tipeslow)
    pyautogui.press('tab',interval=tipeslow)
    pyautogui.press('enter')
    print("Se Cambió la clave... Actualizando fichero de Credenciales")
    
iniciar_sesion(browser)

if verificar_inicio_sesion_exitoso(browser):
    browser.quit()    
    print(f"{mensaje_hora} Inicio de sesión exitoso, se iniciará sesion Real con PYautogui")
    #subprocess.run(['python3', '/home/lmb/spotify/open_spotify_login.py'])
    iniciar_sesion_real_spotify()

elif verificar_inicio_sesion_fallido(browser):
    print(f"{mensaje_hora} Inicio de sesión fallido se cambiará la clave")
    #
    enlace_reset_password = get_link_pwd_change()
    # Comando para abrir Firefox con la URL
    firefox_command = f'firefox {enlace_reset_password}'
    import subprocess
    # Ejecuta el comando en la consola



    # Verificar si la variable tiene un valor de enlace o es None
    if enlace_reset_password is not None:
        # Realizar una tarea o mostrar un mensaje utilizando el valor del enlace
        subprocess.run(firefox_command, shell=True)
        time.sleep(3.1)
        new_new_password_1 = Generate_Password_Account_Spotify()
        new_new_password_2 = new_new_password_1
        enter_repeat_passwd()
        update_credentials(new_new_password_2)

    else:
        # Realizar otra tarea o mostrar otro mensaje si el enlace es None
        print("No se encontró ningún enlace de reseteo de contraseña. Se creará una nueva cuenta.")
    #
    time.sleep(5.1)
    print(f"{mensaje_hora} Inicio de sesión real con PyAutoGUI...")

else:
    # No se pudo determinar el resultado del inicio de sesión
    print(f"{mensaje_hora} No se pudo determinar el resultado del inicio de sesión")

# Cerrar el navegador
browser.quit()