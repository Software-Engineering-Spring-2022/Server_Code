from flask import Flask, render_template, request, flash
import os
import playerEnt
try:
	from flask_sqlalchemy import SQLAlchemy
except:
	os.system("pip install flask_sqlalchemy") #trying to install dependencies if failed
	from flask_sqlalchemy import SQLAlchemy


# -- sample program from this video <https://youtu.be/6plVs_ytIH8>
#  --specific code was created by Matt and james.

app = Flask(__name__)#makes a class for the app or program we wish to run
app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate

# ENV = 'dev'

# if ENV == 'dev':
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://lezbitgtjkbfrs:aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8@ec2-34-206-148-196.compute-1.amazonaws.com:5432/d2gpgbag2bgopb'
# else:
# 	app.debug = False
# 	app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)#connect app to database?

# class Player(db.Model):
# 	__tablename__ = 'player'
# 	id = db.Column(db.Integer)
# 	first_name = db.Column(db.String(30))
# 	last_name  = db.Column(db.String(30))
# 	codename   = db.Column(db.String(30))
	
# 	def __init__(self, first_name, last_name, codename):
# 		self.first_name = first_name
# 		self.last_name  = last_name
# 		self.codename   = codename
# 	def __repr__(self):
# 		return f"dang"
	
@app.route("/")#allows for us to change something when a user uses one of our inputs
def index():
	test_obj = playerEnt.playerEnt(app)
	test_obj.plyr_sc1()
	return render_template("index.html")

# @app.route("/playerEntry2", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
# def playerEntry2():
# 	flash("player entry test")
# 	return render_template("playerEntry2.html")

# @app.route("/edit", methods = ["POST", "GET"]) 
# def edit():
# 	flash("hi " + str(request.form["player_input"]))
# 	id = str(request.form["player_input"])
# 	print(id)
# 	return render_template("playerEntry2.html")
	

# @app.route('/submit', methods=['POST'])#route to submit form,sends information to the database due to POST 
# def submit():
# 	if request.method == 'POST':
# 		id = request.form['id'] #request form gets the data stored 
# 		first_name = request.form['first_name']
# 		last_name = request.form['last_name']
# 		codename = request.form['codename']
		
# 		if db.session.query(Player).filter(Player.id == id).count() == 0:
# 			data = Player(id, first_name, last_name, codename)
# 			db.session.add(data)
# 			db.session.commit()
# 			return render_template('success.html')
# 		return render_template('index.html')
