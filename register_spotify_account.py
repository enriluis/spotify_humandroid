from function_utils_aux import *

def verificar_spotify():
    try:
        # Verificar si Spotify está en ejecución
        subprocess.check_output(['pidof', 'spotify'])
        return True
    except subprocess.CalledProcessError:
        return False
verificar_spotify()
register_spotify_account()
time.sleep(6.1)
#perform_task_with_delay()
#seguir_artist_list_aleatorias()

subprocess.run(['python3', '/home/lmb/spotify/favorite_playlist.py'])

