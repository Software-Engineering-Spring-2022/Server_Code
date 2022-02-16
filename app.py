from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

@app.route("/hello")
def index():
	flash("Hello World")
	return render_template("index.html")

@app.route("/playerEntry")
def playerEntry():
	return render_template("playerEntry.html")
