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

favorite_playlist = os.path.join(script_directory, 'favorite_playlist.py')
subprocess.run(['python3', favorite_playlist])

subprocess.run(['python3', '/home/lmb/spotify/favorite_playlist.py'])