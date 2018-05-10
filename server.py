from flask import Flask, render_template
from getWeather import getData

rainData, windSpeed, windDirection, tempMaxData, tempMinData, descriptionData, imageData = getData()
print(rainData)

app = Flask(__name__)

def getTemp():
    temp = 0
    temp = (9/5)*(temp)+32
    temp = round(temp, 1)
    return (temp)
@app.route("/")    
def index():
    temp = getTemp()
    templateData = {'temperature' : (temp) }
    return render_template("indexr2.html", temperature=temp )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    
