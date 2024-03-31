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
    print(colored("Username:", "yellow"), config.get('Credentials', 'username'))
    print(colored("Password:", "yellow"), config.get('Credentials', 'password'))
    print(colored("Spotify Playlist IDs:", "yellow"), config.get('Play_Lists', 'spotify_playlist_ids'))
    print(colored("Telegram Chat IDs:", "yellow"), config.get('telegram_bot', 'chat_ids'))
    print(colored("Scheduled Hours:", "yellow"), config.get('scheduled_time', 'scheduled_hours'))

def init_config_main():
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), "account.ini"))

    print(colored("Welcome to the configuration setup!", "cyan"))
    print(colored("Please enter the following information:\n", "cyan"))

    username = input(colored("Enter your email address: ", "blue"))
    while not validate_email(username):
        print(colored("Invalid email address. Please try again.", "red"))
        username = input(colored("Enter your email address: ", "blue"))
    config.set('Credentials', 'username', username)

    password = input(colored("Enter your password: ", "blue"))
    config.set('Credentials', 'password', password)

    playlist_ids = input(colored("Enter the Spotify playlist IDs (separated by commas): ", "blue"))
    while not validate_spotify_ids(playlist_ids):
        print(colored("Invalid Spotify playlist IDs. Please try again.", "red"))
        playlist_ids = input(colored("Enter the Spotify playlist IDs (separated by commas): ", "blue"))
    config.set('Play_Lists', 'spotify_playlist_ids', playlist_ids)

    chat_ids = input(colored("Enter the Telegram chat IDs (separated by commas): ", "blue"))
    while not validate_chat_ids(chat_ids):
        print(colored("Invalid Telegram chat IDs. Please try again.", "red"))
        chat_ids = input(colored("Enter the Telegram chat IDs (separated by commas): ", "blue"))
    config.set('telegram_bot', 'chat_ids', chat_ids)

    scheduled_hours = []
    times_count = input(colored("Enter the number of daily schedules: ", "blue"))
    while not times_count.isdigit() or int(times_count) > 4:
        print(colored("Invalid number. Please enter a valid integer (maximum 4).", "red"))
        times_count = input(colored("Enter the number of daily schedules: ", "blue"))
    for i in range(int(times_count)):
        time = input(colored(f"Enter the time for schedule #{i+1} (format HH:MM): ", "blue"))
        while not validate_time(time):
            print(colored("Invalid time format. Please enter the time in HH:MM format.", "red"))
            time = input(colored(f"Enter the time for schedule #{i+1} (format HH:MM): ", "blue"))
        scheduled_hours.append(time)
    config.set('scheduled_time', 'scheduled_hours', ', '.join(scheduled_hours))

    print_confirmation(config)

    save_confirmation = input(colored("\nDo you want to save the configuration? (yes/no): ", "blue"))
    if save_confirmation.lower() == "yes":
        config.set('Credentials', 'is_configured', 'yes')
        update_config_file(config)
        print(colored("\nThe configuration has been successfully updated!", "green"))
    else:
        print(colored("\nThe configuration was not saved.", "yellow"))

if __name__ == '__main__':
    init_config_main()