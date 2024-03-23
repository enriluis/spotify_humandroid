import os, random, time, configparser, os,pyautogui,subprocess
from colorama import Fore, Style
from function_utils_aux import lanzar_spotify, Generate_Password_Account_Spotify,buscar_imagen_y_clic,close_firefox_window,obtener_hora_actual
from function_utils_aux import maximizar_spotify, connect_vpn_randomly,disconnect_vpn,get_active_vpn



tipeslow = random.uniform(500, 1000) / 1000
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"

#subprocess.run(['pkill', 'spotify'])
#print(f"{mensaje_hora} Cerrando cualquier instancia de Spotify que exista abierta")
#active_vpn = get_active_vpn()
#if active_vpn:
#    disconnect_vpn(active_vpn)

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "account.txt"))
your_username = config['Credentials']['username']
your_password = config['Credentials']['password']

email_address = your_username
#print('Password:', password)

# Hacer clic en el Boton de Inicio de sesion en la APP Spotify y 
# Luego se abre el navegador, seguidamente se abre la pagina y 
# se baja ocn tab hasta llegar al enlace de cambio de clave
def spotify_login_click():
    time.sleep(tipeslow)
    if buscar_imagen_y_clic("1_Spotify_Login_Button.png"):
        print(f"{mensaje_hora} Haciendo clic en el login button spotify...")
        time.sleep(8.1)                 # Esperar que abra FireFox
        if buscar_imagen_y_clic("Log_in_to_Spotify.png"):
            print(f"{mensaje_hora} Se detectó la pagina para inicio de sesion ...")
            pyautogui.press('tab',presses=9,interval=tipeslow)  # Bajar por los campos hasta llegar al enlace de Cambiar la Clave
            pyautogui.press('enter')        # Clic para abir enlace con Enter
        else:
            print(f"{mensaje_hora} No se Detectó la pagina, no abrió...")
    else:
        print(f"{mensaje_hora} No se Detectó el boton para hacer clic...")        


def enter_email_address():
    print(f"{mensaje_hora} Insertando la direccion de correo para cambio de clave...")
    if buscar_imagen_y_clic("1_passwd_reset_enter_email.png"):
        pyautogui.typewrite(email_address)
        pyautogui.press('tab')
        pyautogui.press('enter')
        if buscar_imagen_y_clic("2_password_reset_send_mail_notif.png"):
            print(f"{mensaje_hora} Se envió correctamente la direccion  de correo para recibir enlace...")
            time.sleep(tipeslow)
            pyautogui.hotkey('alt', 'f4')     # Simular la pulsación de teclas Alt + F4 Para cerrar Ventana        
    else:
        print(f"{mensaje_hora} No se pudo teclear la direccion de correoo, no se encontro el campo de formulario en pantalla...")


# Abre Spotify
lanzar_spotify()
time.sleep(5.1)
# clic en el boton del Login
spotify_login_click()
time.sleep(3.1)
# Teclea La direccion de correo
enter_email_address()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def get_link_pwd_change():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    browser = webdriver.Firefox()
    try:
        browser.get(url="https://yopmail.com")
        # Ingresa el correo en el campo de entrada
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ycptcpt']/div[2]/div/input"))).send_keys(email_address)
        browser.execute_script("alert('Completa el CAPTCHA manualmente! y presiona ENTER en la CONSOLA al terminar');")
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
        print(f"{mensaje_hora} El elemento no existe o no es visible")
        time.sleep(3.1)
        return None
    finally:
        time.sleep(3.1)
        browser.quit()


new_new_password_1 = Generate_Password_Account_Spotify()
new_new_password_2 = new_new_password_1


# Teclear y Repetir la nuev Clave
def enter_repeat_passwd():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    if buscar_imagen_y_clic("3_password_reset_new_pwd.png"):
        print(f"{mensaje_hora} Detectado Formulario en pantalla, haciendo clic en el...")
        pyautogui.typewrite(new_new_password_1)
        print(f"{mensaje_hora} Tecleando la Nueva Clave")
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.typewrite(new_new_password_2)
        print(f"{mensaje_hora} Repitiendo la Nueva Clave")
        pyautogui.press('tab')
        pyautogui.press('tab')
        print(f"{mensaje_hora} Bajando al Botón con TAB")
        pyautogui.press('enter')
        print(f"{mensaje_hora} Presionando Enter Sobre el Botón para el cambio de Clave")
        time.sleep(tipeslow)
        if not buscar_imagen_y_clic("4_something_wrong_try_again.png"):    # si sale mal algo
            print(f"{mensaje_hora} Ocurrió un problema, reintentando")
            buscar_imagen_y_clic("button_send_password_change.png")        #reintentar mandar el formulario haciendo clic directo en el boton   
            print(f"{mensaje_hora} Clic en el boton Send para Cambiar la Clave.")
        time.sleep(tipeslow)
    elif buscar_imagen_y_clic('password_updated.png'):
        print(f"{mensaje_hora} Se Cambió la Clave Correctamente-1.")
    else:
        print(f"{mensaje_hora} No se encontró el Formulario de cambio de Clave...")


# Actualizar la Clave en el Fichero
def update_credentials(new_password):
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    print(f"{mensaje_hora} Actualizando la clave en el Fichero de configuracion")
    config = configparser.ConfigParser()
    file_path = os.path.join(os.path.dirname(__file__), "account.txt")
    config.read(file_path)
    # Actualiza solo la clave 'Password' en la sección 'Credentials'
    config.set('Credentials', 'Password', new_password)
    with open(file_path, 'w') as config_file:
        config.write(config_file)  # Guarda los cambios en el archivo de configuración


# funcion para iniciar sesion despues de cambiar la Clave
def iniciar_sesion_spotify():
    mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
    subprocess.call(["wmctrl", "-a", "Spotify"])    # Trayendo alfrente la ventana spotify
    time.sleep(tipeslow)
    print(f"{mensaje_hora} Traer al Frente la Ventana de Spotify aplicacion...")
    if buscar_imagen_y_clic('spotify_retry_button.png'):
        print(f"{mensaje_hora} Detectado retry en pantalla, haciendo clic en el...")
        time.sleep(2.1)
        if buscar_imagen_y_clic('1_Spotify_Login_Button.png'):
            print(f"{mensaje_hora} Detectado Login Button en pantalla, haciendo clic en el...")
            time.sleep(6.1)
            print(f"{mensaje_hora} Esperando que abra el navegador para continuar con la app...")
            if buscar_imagen_y_clic('3_Image_Continue_APP.png', grayscale=True, confidence=0.8):       # Click boton Continuar con la APP
                print(f"{mensaje_hora} Detectado Continuar con la APP..click")

            else:
                print(f"{mensaje_hora} No se encontró el boton en la pagina para continuar con la app...")
        else:
            print(f"{mensaje_hora} No se detectó el botón...")
    else:
        print(f"{mensaje_hora} No se detectó Retry en pantalla...")
        subprocess.run(['python3', '/home/lmb/spotify/register_spotify_account.py']) 


enlace_reset_password = get_link_pwd_change()
# Comando para abrir Firefox con la URL
firefox_command = f'firefox {enlace_reset_password} &'


# Verificar si la variable tiene un valor de enlace o es None
if enlace_reset_password is not None:
    # Realizar una tarea o mostrar un mensaje utilizando el valor del enlace
    subprocess.run(firefox_command, shell=True)
    enter_repeat_passwd()
    update_credentials(new_new_password_2)    
    time.sleep(4.9)
    if buscar_imagen_y_clic('password_updated.png'):
        print(f"{mensaje_hora} Se Cambio La Clave correctamente!...")
        time.sleep(tipeslow)
        subprocess.call(["wmctrl", "-a", "Spotify"])    # Traer al Frente la Ventana
        print(f"{mensaje_hora} Trayendo Ventana al frente e iniciar sesion real...")
        iniciar_sesion_spotify()
        
        time.sleep(1.9)
        subprocess.run(['python3', '/home/lmb/spotify/favorite_playlist.py'])
        time.sleep(10.1)
        close_firefox_window()
else:
    # Realizar otra tarea o mostrar otro mensaje si el enlace es None
    print(f"{mensaje_hora} No se encontró ningún enlace de reseteo de contraseña. Se creará una nueva cuenta.")


    


