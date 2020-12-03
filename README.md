# Automatized Discord Custom Status
⛅ Automatized Discord Custom Status using openweathermap.org API 

Remember to 🌟 this Github if you 💖 it.

![a1](https://i.imgur.com/9cdAeg3.png)

## Installation

### [Discord] Get your personal user token - [click here](https://github.com/Tyrrrz/DiscordChatExporter/wiki/Obtaining-Token-and-Channel-IDs#how-to-get-a-user-token)

Copy and paste it in your **config.json** file (`discord_token` field).

### [OpenWeatherMap] Get your application key

You have to get your **openweathermap.org api key**, to allow your app to get the weather of your favourite city. Register [here](https://openweathermap.org/home/sign_up), then go on [your dashboard](https://home.openweathermap.org/api_keys) to get your key. Copy and paste it in your **config.json** file (`weather` field).

### [Crontab] Run the script every 5 minutes

You have to edit the **crontab table** using `crontab -e`. Then, add the following line to this file:  
```sh
*/5 * * * * cd /path/to/auto-discord-bio && /usr/bin/python3 /path/to/auto-discord-bio/main.py >> ~/discord-cron.log 2>&1
```
This will run the script and update your biography every 5 minutes.

### That's it

Congratulations, you have successfully installed Automatized Discord Custom Status. Feel free to open an issue if necessary!
