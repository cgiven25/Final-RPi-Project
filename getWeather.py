#################################################################################A
# Authors: Chris Given, Anna Weeks, Landon Rawson
# Date: 5/3/18
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
    for i in range(4):
        rainData.append(response["daily"]["data"][1+i]["precipProbability"]*100)

    response = requests.get("http://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&APPID={}".format(latitude, longitude, OWMKey))
    response = response.json()

    # We only needed the current wind speed and direction
    windData = response["list"][0]["wind"]
    windSpeed = windData["speed"]
    windDirection = degreesToCardinal(int(windData["deg"]))

    values["windspeed"] = windSpeed
    values["direction"] = windDirection

    # but we need more data for the temperatures, descriptions, and images
    tempMaxData = []
    tempMinData = []
    descriptionData = []
    imageData = []

    # Grab all the temperature data.
    # The API returns information for every three hours over 5 days
    # Grabbing every eighth value makes it grab values for every 24 hours
    for i in range(0, 25, 8):
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

    # put everything in a dictionary to be sent to the template
    for i in range(len(tempMaxData)):
        values["{}Precip".format(i)] = rainData[i]
        values["{}High".format(i)] = tempMaxData[i]
        values["{}Low".format(i)] = tempMinData[i]
        values["{}day".format(i)] = descriptionData[i]
        values["{}img".format(i)] = imageData[i]

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i in range(1, 4):
        # this takes advantage of the fact that you can access elements from the back (negative indices)
        # but you can't go over.
        # the indices will always be negative but that's okay
        values["{}dow".format(i)] = days[i - 7 - date.weekday(date.today())]

    return values
