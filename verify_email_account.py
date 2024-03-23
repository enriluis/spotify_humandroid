import calendar,string, random, time, requests, re, os,subprocess,pyautogui, configparser, datetime
from random import randint, choice, choices
from colorama import Fore, Style
from function_utils_aux import buscar_imagen_y_clic,obtener_hora_actual,read_config,close_firefox_window

your_username, your_password, fecha_creacion, playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()

# Obtener la ruta absoluta del directorio del script
script_directory = os.path.dirname(os.path.abspath(__file__))
enlace_verificar_email = "https://developer.spotify.com/"
# Comando para abrir Firefox con la URL
firefox_command = f'firefox {enlace_verificar_email} &'

pausa = random.uniform(1000, 2000) / 1000
pyautogui.PAUSE = pausa
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"

def verify_email_account():
    """
    Esta función verifica la cuenta de correo electrónico del usuario abriendo Firefox y navegando hasta la página de verificación.
    """
    # Ejecuta el comando para abrir Firefox.
    subprocess.run(firefox_command, shell=True)
    # Imprime un mensaje indicando que se va a confirmar la cuenta de correo.
    print(f"{mensaje_hora} Se va a confirmar la cuenta de correo. Abriendo Firefox")
    # Espera 5.5 segundos para que Firefox se abra.
    time.sleep(5.5)
    # Busca la imagen "verify_spotify_acctount_1.png" y haz clic en ella.
    if buscar_imagen_y_clic("verify_spotify_acctount_Log_In.png", grayscale=True, confidence=0.8):
        # Espera 8.5 segundos para que se abra el formulario de creación de la cuenta.
        time.sleep(8.5)
        if buscar_imagen_y_clic("verify_spotify_acctount_Logo_Log_In.png"):
            # Recorre el formulario de creación de la cuenta y rellena los campos de nombre de usuario y contraseña.
            for _ in range(4):
                pyautogui.press('tab',interval=0.2)
            pyautogui.typewrite(your_username, interval=0.2)
            pyautogui.press('tab')
            pyautogui.typewrite(your_password, interval=0.2)
            time.sleep(3.5)
            # Haz clic en el botón "Entrar".
            for _ in range(3):
                pyautogui.press('tab',interval=0.2)
            pyautogui.press('enter')
            time.sleep(5.5)
            if buscar_imagen_y_clic("verify_spotify_acctount_Dashboard_In_1.png", grayscale=True, confidence=0.8):
                time.sleep(pausa)
                print(f"{mensaje_hora} Entrando al Dashboard")
                if buscar_imagen_y_clic("verify_spotify_acctount_Dashboard_Access.png", grayscale=True, confidence=0.8):
                    time.sleep(pausa)
                    print(f"{mensaje_hora} Entrando al Dashboard")
                    if buscar_imagen_y_clic("verify_spotify_acctount_Acept_Terms.png", grayscale=True, confidence=0.8):
                        time.sleep(pausa)
                        print(f"{mensaje_hora} Click ChekBox Aceptar los terminos")
                        if buscar_imagen_y_clic("verify_spotify_acctount_Acept_Terms_Botton.png", grayscale=True, confidence=0.8):
                            time.sleep(pausa)
                            print(f"{mensaje_hora} Click en el Botón Aceptar los terminos")
                            if buscar_imagen_y_clic("verify_spotify_acctount_Verify_botton.png", grayscale=True, confidence=0.8):
                                time.sleep(pausa)
                                print(f"{mensaje_hora} Click en el botón Verify")
                                if buscar_imagen_y_clic("verify_spotify_acctount_Message_verification_ok.png", grayscale=True, confidence=0.8):
                                    time.sleep(pausa)
                                    print(f"{mensaje_hora} Mensaje de verificacion detectado")
                                    print(f"{mensaje_hora} Cerrar Firefox")
                                else:
                                    print(f"{mensaje_hora} No se encontró el Mensaje de verificacion detectado")
                            else:
                                print(f"{mensaje_hora} No se encontró el botón Verify")
                        else:
                            print(f"{mensaje_hora} No se encontró el Botón Aceptar los terminos")
                    else:
                        print(f"{mensaje_hora} No se encontró la imagen")
                else:
                    print(f"{mensaje_hora} No se encontró la imagen")
            else:
                print(f"{mensaje_hora} No se encontró la imagen")
        else:
            print(f"{mensaje_hora} No se encontró la imagen")
    else:
        print(f"{mensaje_hora} No se encontró la imagen")

verify_email_account()
time.sleep(5.1)

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
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='ycptcpt']/div[2]/div/input"))).send_keys(your_username)
        browser.execute_script("alert('Completa el CAPTCHA manualmente! y presiona ENTER en la CONSOLA al terminar');")
        input("Presiona ENTER cuando hayas completado el captcha...")
        frame = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.ID, 'ifmail')))
        browser.switch_to.frame(frame)        

        time.sleep(2.1)
        element = browser.find_element(By.XPATH,"//div[@id='mail']/div/table/tbody/tr/td/div/table[4]/tbody/tr[2]/td[2]/table/tbody/tr/td/div/a/table/tbody/tr/td[2]")
        element.click()
        #reset_password_link = browser.find_element(By.XPATH, "//p[contains(.,'Thanks for confirming your email address.')]")
        #reset_password_href = reset_password_link.get_attribute('href')
        #return reset_password_href
    except TimeoutException:
        # El elemento no existe o no es visible
        print(f"{mensaje_hora} El elemento no existe o no es visible")
        time.sleep(5.1)
        return None
    finally:
        time.sleep(5.1)
        browser.quit()

get_link_pwd_change()
