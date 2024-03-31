# spotify_robot
A small Python robot that listens to and plays music in your place, using a D-Bus connection in Linux to control the Spotify app. It simulates being human by performing actions like playing, stopping, pausing, rotating, and more! It also retrieves statistics and sends them to your favorite Telegram bot.

Before starting, make sure you have the Spotify app installed on Linux. This script will create a Spotify account by interacting with your Linux desktop. I recommend installing it on a small virtual machine to avoid errors and interruptions during the account creation process and other actions.

Of course, you need to have a Spotify account. The 'register_spotify_account.py' script will create an account for you. The account creation process involves real and organic interaction with the desktop environment and applications.

To play your favorite playlist, add it to the 'spotify_account.txt' file located in the script folder and schedule the time when you want it to play. During the remaining time, it will stop, and an empty function will be called, resulting in no action.

After each round of playing your favorite playlist, the script will retrieve the statistics and send them to your Telegram Chat. You must identify the Chat ID and provide it in the configuration file.

This github repo is for EDUCATIONAL AND TESTING PURPOSES ONLY. I am NOT under any responsibility if a problem occurs.
