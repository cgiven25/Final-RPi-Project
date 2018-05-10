#################################################################################
# Authors: Chris Given, Anna Weeks, Landon Rawson
# Date: 5/3/18
# Description: Gets the current relevant weather data from the API below
# [obligatory shilling]: Powered by Dark Sky (https://darksky.net/poweredby/)
#################################################################################
import requests
import sys

# ---- IMPORTANT VALUES ---- #
# windSpeed, windDirection
# tempMaxData, tempMinData
# descriptionData
# imageData

# I found this on github: https://gist.github.com/RobertSudwarts/acf8df23a16afdb5837f
# This is very approximate but it will work for our purposes
def degreesToCardinal(deg):
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = int((deg + 11.25)/22.5)
    return dirs[ix % 16]

def getData():
    # ---- KEYS ---- #
    DSKey = open("DARKSKY_KEY.txt", "r").read().strip("\n")
    OWMKey = open("OPEN_WEATHER_KEY.txt", "r").read().strip("\n")

    # The latitude and longitude for Ruston
    latitude = 32.5232
    longitude = -92.6379

    # Gets the rain chance from the Dark Sky API
    response = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(DSKey, latitude, longitude))
    response = response.json()
    rainChance = response["minutely"]["data"][0]["precipProbability"]

    response = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}".format(latitude, longitude, OWMKey))
    response = response.json()

    # We only needed the current wind speed and direction
    windData = response["list"][0]["wind"]
    windSpeed = windData["speed"]
    windDirection = degreesToCardinal(int(windData["deg"]))

    # but we need more data for the temperatures, descriptions, and images
    tempMaxData = []
    tempMinData = []
    descriptionData = []
    imageData = []

    # Grab all the temperature data.
    # The API returns information for every three hours over 5 days
    # Grabbing every eighth value makes it grab values for every 24 hours
    for i in range(0, len(response["list"]), 8):
        tempMinData.append(response["list"][i]["main"]["temp_min"])
        tempMaxData.append(response["list"][i]["main"]["temp_max"])
        descriptionData.append(response["list"][i]["weather"][0]["description"])
        imageData.append(response["list"][i]["weather"][0]["icon"])

    # Get the url of each icon and replace it with the icon code
    for i in range(len(imageData)):
        imageData[i] = "http://openweathermap.org/img/w/{}.png".format(imageData[i])

    for i in range(len(tempMinData)):
        # converts the temperatures to Fahrenheit (they were in Kelvin)
        tempMinData[i] = (int(tempMinData[i]) - 273) * 9 / 5 + 32
        tempMaxData[i] = (int(tempMaxData[i]) - 273) * 9 / 5 + 32 

    return windSpeed, windDirection, tempMaxData, tempMinData, descriptionData, imageData
