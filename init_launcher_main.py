import time,subprocess,requests,random,os,configparser,threading,re,json,datetime
from spotify_monitor import verificar_y_abrir_spotify, obtener_ids_playlist, playlist_favorite_scheduler
from config_assistant import init_config_main
from function_utils_aux import obtener_hora_actual
from colorama import Fore, Style

script_directory = os.path.dirname(os.path.abspath(__file__))
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"


def check_configuration():
    config = configparser.ConfigParser()
    config_file = os.path.join(os.path.dirname(__file__), "account.ini")
    config.read(config_file)

    is_configured = config.get("Credentials", "is_configured").lower()
    if is_configured == "yes":
        print(f"{mensaje_hora} The script is configured!!!!")
    elif is_configured == "no":
        print(f"{mensaje_hora} The script is not configured. Launching the configuration assistant...")
        if __name__ == '__main__':
            init_config_main()
    else:
        print(f"{mensaje_hora} The value of the 'is_configured' field in the configuration file is invalid.")
        

        
if __name__ == '__main__':
    check_configuration()
    verificar_y_abrir_spotify()
    playlist_ids = obtener_ids_playlist()

    playlist_thread = threading.Thread(target=playlist_favorite_scheduler, args=(playlist_ids,))
    playlist_thread.start()    

    