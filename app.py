from flask import Flask, render_template, request, flash
import time

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route("/")
def index():
	flash("Hello World")
	return render_template("index.html")

time.sleep(5)

@app.route("/playerEntry")
def playerEntry():
	return render_template("playerEntry.html")
