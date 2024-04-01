import re
import os
from configparser import ConfigParser
from termcolor import colored
from colorama import Fore, Style
from function_utils_aux import obtener_hora_actual

mensaje_hora = f"[{Fore.GREEN}{obtener_hora_actual()}{Style.RESET_ALL}]"

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_spotify_ids(ids):
    id_list = ids.split(',')
    if len(id_list) > 4:
        return False
    for playlist_id in id_list:
        if len(playlist_id) != 22 or not playlist_id.isalnum():
            return False
    return True

def validate_chat_ids(ids):
    id_list = ids.split(',')
    for chat_id in id_list:
        if len(chat_id) != 9 or not chat_id.isdigit():
            return False
    return True

def validate_time(time):
    pattern = r'^([01]\d|2[0-3]):([0-5]\d)$'
    return re.match(pattern, time)

def update_config_file(config):
    with open(os.path.join(os.path.dirname(__file__), "account.ini"), 'w') as configfile:
        config.write(configfile)

def print_confirmation(config):
    print(colored("\nPlease verify the entered data:", "green"))
    print(colored("Username:", "yellow"), f"{config.get('Credentials', 'username')} [{Fore.YELLOW}Current: {config.get('Credentials', 'username')}{Style.RESET_ALL}]")
    print(colored("Password:", "yellow"), f"{config.get('Credentials', 'password')} [{Fore.YELLOW}Current: {config.get('Credentials', 'password')}{Style.RESET_ALL}]")
    print(colored("Spotify Playlist IDs:", "yellow"), f"{config.get('Play_Lists', 'spotify_playlist_ids')} [{Fore.YELLOW}Current: {config.get('Play_Lists', 'spotify_playlist_ids')}{Style.RESET_ALL}]")
    print(colored("Telegram Chat IDs:", "yellow"), f"{config.get('telegram_bot', 'chat_ids')} [{Fore.YELLOW}Current: {config.get('telegram_bot', 'chat_ids')}{Style.RESET_ALL}]")
    print(colored("Scheduled Hours:", "yellow"), f"{config.get('scheduled_time', 'scheduled_hours')} [{Fore.YELLOW}Current: {config.get('scheduled_time', 'scheduled_hours')}{Style.RESET_ALL}]")

def init_config_main():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))
    
    print(colored("Welcome to the configuration setup!", "cyan"))
    print(colored("Please enter the following information:\n", "cyan"))
    current_username = f"{Fore.YELLOW}[{config.get('Credentials', 'username')}]{Style.RESET_ALL}"
    username = input(colored(f"Enter your email address {current_username}: ", "blue")) 
    if username.strip() == "":
        username = config.get('Credentials', 'username')
    while not validate_email(username):
        print(colored("Invalid email address. Please try again.", "red"))        
        username = input(colored(f"Enter your email address (e.g., example@example.com) The current account/email is{current_username}: ", "blue"))
    config.set('Credentials', 'username', username)
    current_password = f"{Fore.YELLOW}[{config.get('Credentials', 'password')}]{Style.RESET_ALL}"
    password = input(colored(f"Enter your password {current_password}: ", "blue"))
    if password.strip() == "":
        password = config.get('Credentials', 'password')
    config.set('Credentials', 'password', password)

    playlist_ids = input(colored("Enter the Spotify playlist IDs (separated by commas): ", "blue"))
    if playlist_ids.strip() == "":
        playlist_ids = config.get('Play_Lists', 'spotify_playlist_ids')
    while not validate_spotify_ids(playlist_ids):
        print(colored("Invalid Spotify playlist IDs. Please try again.", "red"))
        playlist_ids = input(colored("Enter the Spotify playlist IDs (e.g., playlist1,playlist2): ", "blue"))
    config.set('Play_Lists', 'spotify_playlist_ids', playlist_ids)

    chat_ids = input(colored("Enter the Telegram chat IDs (separated by commas): ", "blue"))
    if chat_ids.strip() == "":
        chat_ids = config.get('telegram_bot', 'chat_ids')
    while not validate_chat_ids(chat_ids):
        print(colored("Invalid Telegram chat IDs. Please try again.", "red"))
        chat_ids = input(colored("Enter the Telegram chat IDs (e.g., chat1,chat2): ", "blue"))
    config.set('telegram_bot', 'chat_ids', chat_ids)

    scheduled_hours = []
    times_count = input(colored("Enter the number of daily schedules[1-4]: ", "blue"))
    if times_count.strip() == "":
        times_count = len(config.get('scheduled_time', 'scheduled_hours').split(','))
    while not times_count.isdigit() or int(times_count) > 4:
        print(colored("Invalid number of daily schedules. Please try again.", "red"))
        times_count = input(colored("Enter the number of daily schedules (1-4): ", "blue"))
    times_count = int(times_count)
    for i in range(times_count):
        time = input(colored(f"Enter scheduled time {i+1} (HH:MM): ", "blue"))
        if time.strip() == "":
            time = config.get('scheduled_time', f'scheduled_hour_{i+1}')
        while not validate_time(time):
            print(colored("Invalid time format. Please enter the time in HH:MM format.", "red"))
            time = input(colored(f"Enter scheduled time {i+1} (HH:MM): ", "blue"))
        scheduled_hours.append(time)
        #config.set('scheduled_time', f'scheduled_hour_{i+1}', time)
        config.set('scheduled_time', 'scheduled_hours', ",".join(scheduled_hours))

    print_confirmation(config)

    update_config_file(config)

def check_configuration():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))

    if not config.has_section('Credentials') or not config.has_section('Play_Lists') or not config.has_section('telegram_bot') or not config.has_section('scheduled_time'):
        init_config_main()
    else:
        if not config.has_option('Credentials', 'username') or not config.has_option('Credentials', 'password') or not config.has_option('Play_Lists', 'spotify_playlist_ids') or not config.has_option('telegram_bot', 'chat_ids') or not config.has_option('scheduled_time', 'scheduled_hours'):
            init_config_main()
        else:
            username = config.get('Credentials', 'username')
            password = config.get('Credentials', 'password')
            playlist_ids = config.get('Play_Lists', 'spotify_playlist_ids')
            chat_ids = config.get('telegram_bot', 'chat_ids')
            scheduled_hours = config.get('scheduled_time', 'scheduled_hours')

            if username.strip() == "" or password.strip() == "" or playlist_ids.strip() == "" or chat_ids.strip() == "" or scheduled_hours.strip() == "":
                init_config_main()

def main():
    try:
        check_configuration()
    except Exception as e:
        print(f"{mensaje_hora} {Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()