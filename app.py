from flask import Flask
from flask import render_template
from markupsafe import escape


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html') 