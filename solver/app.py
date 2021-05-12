from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Oh-h-h...it's T-o-C......."
