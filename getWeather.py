import requests
import sys

response = requests.get("http://api.openweathermap.org/data/2.5/weather?id=4339348&APPID=5d5431efbe7c1d275a766270e8fb8e72")
response = response.content
sys.stdout.write(str(response))

