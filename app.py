#######################################################################
# Authors: Chris Given, Anna Weeks, Landon Rawson
# Date: 5/15/18
# Description: Gets the weather data from the getWeather module
#              and sends it to the server
#              Hosts an html template on the public ip address
#              of the machine running this program.
#######################################################################

from flask import Flask, render_template
from getWeather import getData
from getSensor import getTemp, getHumd
app = Flask(__name__)

@app.route("/")
def index():
    data = getData()
    data['temperature']=getTemp()
    data['humidity']=getHumd()
    return render_template("index.html", **data)

if __name__ == "__main__":
    app.run(debug = True, host="138.47.134.89")
