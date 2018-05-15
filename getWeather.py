#################################################################################A
# Authors: Chris Given, Anna Weeks, Landon Rawson
# Date: 5/15/18
# Description: Gets the current relevant weather data from the API below
# [obligatory shilling]: Powered by Dark Sky (https://darksky.net/poweredby/)
#################################################################################
import requests
import sys
from datetime import date

# ---- IMPORTANT VALUES ---- #
# rainData
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
    values = {}

    # ---- KEYS ---- #
    DSKey = open("DARKSKY_KEY.txt", "r").read().strip("\n")
    OWMKey = open("OPEN_WEATHER_KEY.txt", "r").read().strip("\n")

    # The latitude and longitude for Ruston
    latitude = 32.5232
    longitude = -92.6379

    # Gets the rain chance from the Dark Sky API
    response = requests.get("https://api.darksky.net/forecast/{}/{},{}".format(DSKey, latitude, longitude))
    response = response.json()
    rainData = []
    rainData.append(response["currently"]["precipProbability"]*100)
    tempMinData = []
    tempMaxData = []
    for i in range(4):
        rainData.append(response["daily"]["data"][i]["precipProbability"]*100)
        tempMinData.append(response["daily"]["data"][i]["apparentTemperatureMin"])
        tempMaxData.append(response["daily"]["data"][i]["apparentTemperatureMax"])

    response = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}".format(latitude, longitude, OWMKey))
    response = response.json()

    # We only needed the current wind speed and direction
    windData = response["list"][0]["wind"]
    windSpeed = windData["speed"]
    windDirection = degreesToCardinal(int(windData["deg"]))

    values["windspeed"] = windSpeed
    values["direction"] = windDirection

    # but we need more data for the temperatures, descriptions, and images
    descriptionData = []
    imageData = []

    # Grab all the temperature data.
    # The API returns information for every three hours over 5 days
    # Grabbing every eighth value makes it grab values for every 24 hours
    for i in range(0, 40, 8):
        descriptionData.append(response["list"][i]["weather"][0]["description"])
        imageData.append(response["list"][i]["weather"][0]["icon"])

    # Get the url of each icon and replace it with the icon code
    for i in range(len(imageData)):
        imageData[i] = "http://openweathermap.org/img/w/{}.png".format(imageData[i])

    # put everything in a dictionary to be sent to the template
    for i in range(len(tempMaxData)):
        values["Precip{}".format(i)] = round(rainData[i], 2)
        values["High{}".format(i)] = round(tempMaxData[i], 1)
        values["Low{}".format(i)] = round(tempMinData[i], 1)
        values["desc{}".format(i)] = descriptionData[i]
        values["img{}".format(i)] = imageData[i]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(1, 4):
        # this takes advantage of the fact that you can access elements from the back (negative indices)
        # but you can't go over.
        # the indices will always be negative but that's okay
        values["dow{}".format(i)] = days[(date.weekday(date.today()) + i) % 7]

    return values
