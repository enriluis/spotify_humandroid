from function_utils_aux import *

def verificar_spotify(): 
    try:
        # Verificar si Spotify está en ejecución
        subprocess.check_output(['pidof', 'spotify'])
        return True
    except subprocess.CalledProcessError:
        return False
verificar_spotify()
    
iniciar_sesion_real_spotify()
time.sleep(15)
perform_task_with_delay()
#seguir_artist_list_aleatorias()
subprocess.run(['python3', '/home/lmb/spotify/spotify_monitor.py'])

