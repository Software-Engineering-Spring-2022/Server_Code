from flask import Flask, render_template, request, flash
from flask import flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "manbearpig_MUDMAN888"

ENV = 'dev'

if ENV == 'dev':
	app.debug = True
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lezbitgtjkbfrs:aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8@ec2-34-206-148-196.compute-1.amazonaws.com:5432/d2gpgbag2bgopb
else:
	app.debug = False
	app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Player(db.Model):
	__tablename__ = 'player'
	id = db.Column(db.Integer)
	first_name = db.Column(db.String(30))
	last_name  = db.Column(db.String(30))
	codename   = db.Column(db.String(30))
	
	def __init__(self, first_name, last_name, codename):
		self.first_name = first_name
		self.last_name  = last_name
		self.codename   = codename
	
@app.route("/")
def index():
	flash("Hello World")
	return render_template("index.html")

@app.route("/playerEntry")
def playerEntry():
	return render_template("playerEntry.html")

@app.route('/submit', methods=['POST'])
def submit():
	if request.method == 'POST':
		id = request.form['id']
		first_name = request.form['first_name']
		last_name = request.form['last_name']
		codename = request.form['codename']
		
		if db.session.query(Player).filter(Player.id == id).count() == 0:
			data = Player(id, first_name, last_name, codename)
			db.session.add(data)
			db.session.commit()
			--return render_template('success.html')
		return render_template('index.html')
