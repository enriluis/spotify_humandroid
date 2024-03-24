from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual,read_config
import spotipy,sys,time,os
from spotipy.oauth2 import SpotifyClientCredentials

import configparser

os.environ['DISPLAY'] = ':0'
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"
if len(sys.argv) == 4:
    # Cargar los argumentos como variables
    playlist_id = sys.argv[1]
    nombre_playlist = str(sys.argv[2])
    playlist_duration = str(sys.argv[3])
else:
    # Cargar las variables desde el archivo
    your_username, your_password, fecha_creacion,playlist_id, nombre_playlist, playlist_duration,virtual_machine = read_config()

def obtener_info_playlist_from_spotify(playlist_id):
    # Configurar las credenciales del cliente de Spotify
    client_id = 'ee204ef35a9f4ae3affce9400fda2c2a'
    client_secret = '46696c68f11f4a85807f6c030a6598e7'    
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    try:
        # Obtener los detalles de la playlist utilizando su ID
        playlist = sp.playlist(playlist_id)
        total_duration_ms = 0
        tracks = []  # Lista para almacenar los tracks de la playlist

        # Obtener todos los tracks de la playlistame, artists(name), duration_ms)), total')
        playlist_tracks = results['items']

        while 'next' in results and results['next']:
            results = sp.next(results)
            playlist_tracks.extend(results['items'])

        for track in playlist_tracks:
            track_info = track['track']
            if track_info is not None:  # Verificar que track_info no sea None
                total_duration_ms += track_info['duration_ms']
                track_name = track_info['name']
                artist_names = [artist['name'] for artist in track_info['artists']]
                duration_minutes = (track_info['duration_ms'] // 1000 // 60) + 1
                tracks.append({'nombre': track_name, 'artistas': artist_names, 'duracion': duration_minutes})

        playlist_duration_minutes = (total_duration_ms // 1000 // 60) + 1
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']
        playlist_cover_image = playlist['images'][0]['url']

        # Crear el objeto ConfigParser y agregar los datos a la sección 'Playlist'
        config = configparser.ConfigParser()
        config['Playlist'] = {
            'nombre': playlist_name,
            'duracion': str(playlist_duration_minutes),
            'url': playlist_url,
            'imagen_portada': playlist_cover_image
        }

        # Agregar cada track a la sección 'Tracks'
        for i, track in enumerate(tracks):
            track_section = 'Track{}'.format(i + 1)
            config[track_section] = track
        config_file_path = os.path.join(os.path.dirname(__file__), "playlists", playlist_id + ".ini")
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)

        return {
            'nombre': playlist_name,
            'duracion': playlist_duration_minutes,
            'url': playlist_url,
            'imagen_portada': playlist_cover_image,
            'tracks': tracks  # Agregar la lista de tracks a la respuesta
        }
    except spotipy.SpotifyException as e:
        # Si ocurre una excepción de conexión, esperar 5 segundos y continuar sin hacer cambios
        print("Se produjo un error de conexión. Se mostrará una advertencia y se continuará sin hacer cambios.")
        time.sleep(5)
        return None
