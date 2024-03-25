from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual,read_config
import spotipy,sys,time,os
from spotipy.oauth2 import SpotifyClientCredentials
import configparser

os.environ['DISPLAY'] = ':0'
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"

if len(sys.argv) == 2:
    playlist_id = sys.argv[1]
else:
    your_username, your_password,creation_date,playlist_id,virtual_machine,bot_token,bot_chat_ids, spotify_client_id, spotify_client_secret = read_config()

def obtener_info_playlist_from_spotify(playlist_id):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))
    client_id = config.get('spotify_credentials','client_id')
    client_secret = config('spotify_credentials','secret')
    credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    try:
        playlist = sp.playlist(playlist_id)
        total_duration_ms = 0
        tracks = []
        playlist_tracks = results['items']

        while 'next' in results and results['next']:
            results = sp.next(results)
            playlist_tracks.extend(results['items'])

        for track in playlist_tracks:
            track_info = track['track']
            if track_info is not None:
                total_duration_ms += track_info['duration_ms']
                track_name = track_info['name']
                artist_names = [artist['name'] for artist in track_info['artists']]
                duration_minutes = (track_info['duration_ms'] // 1000 // 60) + 1
                tracks.append({'nombre': track_name, 'artistas': artist_names, 'duracion': duration_minutes})

        playlist_duration_minutes = (total_duration_ms // 1000 // 60) + 1
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']
        playlist_cover_image = playlist['images'][0]['url']

        config = configparser.ConfigParser()
        config['Playlist'] = {
            'nombre': playlist_name,
            'duracion': str(playlist_duration_minutes),
            'url': playlist_url,
            'imagen_portada': playlist_cover_image
        }

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
            'tracks': tracks
        }
    except spotipy.SpotifyException as e:
        print("Se produjo un error de conexión. Se mostrará una advertencia y se continuará sin hacer cambios.")
        time.sleep(5)
        return None
