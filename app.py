from flask import Flask, render_template, request, flash
import os
import playerEnt
import psycopg2
from config import config

# -- sample program from this video <https://youtu.be/6plVs_ytIH8>
#  --specific code was created by Matt and james.

app = Flask(__name__)#makes a class for the app or program we wish to run
app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate

def insert_player(id, first_name, last_name, codename):	# Call this to insert players into the database table player
	""" insert a new player int players table """
	sql = """INSERT INTO player(id, first_name, last_name, codename)
		 VALUES(id, first_name, last_name, codename);"""
	conn = None
	try:
		conn = psycopg2.connect( # connects to database
			host="ec2-34-206-148-196.compute-1.amazonaws.com"
			database="d2gpgbag2bgopb"
			user="lezbitgtjkbfrs"
			password="aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8"
		)
		cur = conn.cursor() # creating cursor object

		cur.execute(sql, (id, first_name, last_name, codename)) # execute the INSERT command
		
		conn.commit() # commit the changes to the database
		
		cur.close() # close communication with the database
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


# Testing insert player function
insert_player(2, 'Matt', 'Clemence', 'Shark')
			
			
@app.route("/")#allows for us to change something when a user uses one of our inputs
def index():
	test_obj = playerEnt.playerEnt(app)
	test_obj.plyr_sc1(app)
	render_template("playerEntry2.html")
	

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

# 		return render_template('index.html')
