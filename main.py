# Used to make call to the Discord API
import requests

# Used to read the config file
import json

# Used to display the last update
from datetime import datetime

# Read the config file
with open("config.json", "r") as f:
    config = json.load(f)

# https://openweathermap.org/weather-conditions
weather_codes = {
    # Code - Icon
    "200": "11",
    "201": "11",
    "202": "11",
    "210": "11",
    "211": "11",
    "212": "11",
    "221": "11",
    "230": "11",
    "231": "11",
    "232": "11",
    "300": "09",
    "301": "09",
    "302": "09",
    "310": "09",
    "311": "09",
    "312": "09",
    "313": "09",
    "314": "09",
    "321": "09",
    "500": "10",
    "501": "10",
    "502": "10",
    "503": "10",
    "504": "10",
    "511": "13",
    "520": "09",
    "521": "09",
    "522": "09",
    "531": "09",
    "600": "13",
    "601": "13",
    "602": "13",
    "611": "13",
    "612": "13",
    "613": "13",
    "615": "13",
    "616": "13",
    "620": "13",
    "621": "13",
    "622": "13",
    "701": "50",
    "711": "50",
    "721": "50",
    "731": "50",
    "741": "50",
    "751": "50",
    "761": "50",
    "762": "50",
    "771": "50",
    "781": "50",
    "800": "01",
    "801": "02",
    "802": "03",
    "803": "04",
    "804": "04"
}

weather_emojis = {
    # d > day | n > night
    "01": {
        "d": {
            "emoji_name": "☀️"
        },
        "n": {
            "emoji_name": "🌑"
        }
    },
    "02": {
        "d": {
            "emoji_name": "🌥️"
        },
        "n": {
            "emoji_name": "☁"
        }
    },
    "03": {
        "d": {
            "emoji_name": "☁"
        },
        "n": {
            "emoji_name": "☁"
        }
    },
    "04": {
        "d": {
            "emoji_name": "☁"
        },
        "n": {
            "emoji_name": "☁"
        }
    },
    "09": {
        "d": {
            "emoji_name": "🌧️"
        },
        "n": {
            "emoji_name": "🌧️"
        }
    },
    "10": {
        "d": {
            "emoji_name": "🌧️"
        },
        "n": {
            "emoji_name": "🌧️"
        }
    },
    "11": {
        "d": {
            "emoji_name": "🌩️"
        },
        "n": {
            "emoji_name": "🌩️"
        }
    },
    "13": {
        "d": {
            "emoji_name": "❄️"
        },
        "n": {
            "emoji_name": "❄️"
        }
    },
    "50": {
        "d": {
            "emoji_name": "🌫️"
        },
        "n": {
            "emoji_name": "🌫️"
        }
    },
}

def update_custom_status(text, emoji):
    """
    Update the Discord Custom Status of the user

    Args:
        text (str): The new custom status content

    Returns:
        data (any): The Discord response
    """

    custom_status = {'custom_status':{'text': text, 'emoji_name': emoji}}

    url = "https://discordapp.com/api/v6/users/@me/settings"
    headers = {
        "Authorization": config["discord_token"],
        "Content-Type": "application/json",
    }
    response = requests.patch(url, json.dumps(custom_status), headers=headers)
    data = response.json()
    return data

def get_weather_of(city):
    """
    Get the weather of a specific city

    Args:
        city (str): The name of the city whose weather we want

    Returns:
        weather (str): The weather of the city
    """
    # Open Weather Map API Base url
    base_url = (
        "http://api.openweathermap.org/data/2.5/weather?appid="
        + config["weather"]
        + "&q="
        + city
        + "&units="
        + config["units"]
    )
    response = requests.get(base_url)
    data = response.json()
    # Returns weather info
    return data

def generate_custom_status_content(weather):
    """
    Generate the custom status content

    Args:
        weather (str): The weather of the city

    Returns:
        custom_status_content (str): The final custom status content
    """
    # The current time (hours and minutes)
    now = datetime.now().strftime("%I:%M %p")

    # Some useful variables
    desc = weather["weather"][0]["description"]
    temp = round(weather["main"]["temp"])
    temp_symbol = (
        "°C"
        if config["units"] == "metric"
        else "°F"
        if config["units"] == "imperial"
        else "K"
    )
    feels_like = round(weather["main"]["feels_like"])
    city = config["city"]

    # Returns the final string wich contain the city, the current temp, the felt temp, the weather, the last update and the credits
    return (
        "Current weather in "
        + city
        + ": "
        + str(temp)
        + str(temp_symbol)
        + ". "
        + "Feels like "
        + str(feels_like)
        + str(temp_symbol)
        + ". "
        + str(desc.upper())
        + " | Last update: "
        + now
        + " | Made using Python"
    )

def resolve_icon(weather):
    """
    Resolve the weather icon
    Args:
        weather (str): The weather object
    Returns:
        emoji (str): The emoji name
    """
    weather_id = str(weather["weather"][0]["id"])
    day_or_night = str(weather["weather"][0]["icon"][2:])

    emoji = '☁'

    if weather_id in weather_codes:
        if weather_codes[weather_id] in weather_emojis:
            emoji = weather_emojis[weather_codes[weather_id]][day_or_night]['emoji_name']

    return emoji

def main():
    """
    Main code which call the other functions
    """
    # Get the weather of the city
    weather = get_weather_of(config["city"])
    # Get the custom status content
    custom_status_content = generate_custom_status_content(weather)
    # Get the weather emoji
    weather_emoji = resolve_icon(weather)
    # Update the Custom Status
    status = update_custom_status(custom_status_content, weather_emoji)
    # Log
    log_prefix = "[" + datetime.now().strftime("%I:%M %p") + "]"

    if "locale" in status:
        print(log_prefix + " Successfully updated custom status.")

    else:
        # If Discord returned a message
        if "message" in status:
            # If the error is caused by the personal access token
            if status["message"] == "401: Unauthorized":
                print(
                    log_prefix
                    + " Seems like your Discord personal access token is invalid..."
                )
            else:
                print(
                    log_prefix
                    + " Something happened. Message is the following: "
                    + status["message"]
                )
        # If Discord didn't return anything
        else:
            print(
                log_prefix
                + " Something happened. Here is the Discord API response: "
                + status["message"]
            )


if __name__ == "__main__":
    main()
