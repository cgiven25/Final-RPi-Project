from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def index():
    print "Hi"
    return "sup"

def getData():
    return "30%", "65F", "HIGH"

@app.route("/data")
def hello():
    precip, temp, pollen = getData()
    return render_template("page.html", precip = precip, temp = temp, pollen = pollen)

if __name__ == "__main__":
    app.run()
