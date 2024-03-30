from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual,obtener_ids_playlist
import spotipy,sys,time,os
from spotipy.oauth2 import SpotifyClientCredentials
import configparser

os.environ['DISPLAY'] = ':0'
mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"

if len(sys.argv) == 2:
    playlist_id = sys.argv[1]
else:
    playlist_id = obtener_ids_playlist()

def obtener_info_playlist_from_spotify(playlist_id):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini")) 
    client_id = config.get('spotify_credentials', 'client_id')
    client_secret = config.get('spotify_credentials', 'client_secret')  
    credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials_manager)

    try:
        playlist = sp.playlist(playlist_id)
        total_duration_ms = 0
        tracks = []
        results = playlist['tracks']

        while True:
            playlist_tracks = results['items']

            for track in playlist_tracks:
                track_info = track['track']
                if track_info is not None:
                    total_duration_ms += track_info['duration_ms']
                    track_name = track_info['name']
                    artist_names = [artist['name'] for artist in track_info['artist']]
                    duration_minutes = (track_info['duration_ms'] // 1000 // 60) + 1
                    tracks.append({'name': track_name, 'artist': artist_names, 'duration': duration_minutes})

            if results['next']:
                results = sp.next(results)
            else:
                break

        playlist_duration_minutes = (total_duration_ms // 1000 // 60) + 1
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']
        playlist_cover_image = playlist['images'][0]['url']

        config = configparser.ConfigParser()
        config['Playlist'] = {
            'name': playlist_name,
            'duration': str(playlist_duration_minutes),
            'url': playlist_url,
            'image_thumb': playlist_cover_image
        }

        for i, track in enumerate(tracks):
            track_section = 'Track{}'.format(i + 1)
            config[track_section] = track
        config_file_path = os.path.join(os.path.dirname(__file__), "playlists", playlist_id + ".ini")
        with open(config_file_path, 'w') as configfile:
            config.write(configfile)
        print(f"{mensaje_hora} Updated playlist {Fore.YELLOW}{playlist_name}{Style.RESET_ALL} info from spotify API in to {Fore.RED}{config_file_path}{Style.RESET_ALL}")
        return {
            'name': playlist_name,
            'duration': playlist_duration_minutes,
            'url': playlist_url,
            'image_thumb': playlist_cover_image,
            'tracks': tracks
        }
    except spotipy.SpotifyException as e:
        print(f"{mensaje_hora} An error occurred.")
        time.sleep(5)
        return None
    
for playlist_id in obtener_ids_playlist():
    obtener_info_playlist_from_spotify(playlist_id)
