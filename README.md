# Final-RPi-Project
This project is a weather app - something you can easily manage and view that keeps track of the day-to-day weather.

Some of the capabilities come from a Raspberry Pi model 3B+.  These include:
  Current temperature
  Humidity

The other information is found by polling two APIs:
  Dark Sky API (this app is powered by the Dark Sky: https://darksky.net/poweredby/) and Openweathermap
  
  Openweathermap provided us with:
    Wind speed,
    Wind Direction,
    Descriptions of the weather,
    Images to match descriptions.
  
  Dark Sky provided us with:
    Chance of precipitation,
    Temperature High and Low
 
Note: The singular app.py file listed in the repo will not work without a SenseHat for the Raspberry Pi.

webapp.zip has some external dependencies: Flask and requests libraries for Python and the two API keys used to poll the APIs.  I'm not posting them because my account can be locked/charged for excessive polling.
