from flask import Flask, render_template, request, flash, redirect, url_for
import os
import time
os.system("pip install psycopg2-binary")
import psycopg2
# -- sample program from this video <https://youtu.be/6plVs_ytIH8>
#  --specific code was created by Matt and james.

app = Flask(__name__)#makes a class for the app or program we wish to run
app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate
i = 0

def config():
	conn = None
	try:
		conn = psycopg2.connect( # connects to database
				user="lezbitgtjkbfrs",
				password="aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8",
				host="ec2-34-206-148-196.compute-1.amazonaws.com",
				port="5432",
				database="d2gpgbag2bgopb")
	except (Exception, psycopg2.DatabseError) as error:
			print(error)
	finally:
			if conn is not None:
					conn.close()
					
	return conn

def insert_player(ID, FIRST_NAME, LAST_NAME, CODENAME):	# Call this to insert players into the database table player
	conn = None
	try:
		conn = psycopg2.connect( # connects to database
			user="lezbitgtjkbfrs",
			password="aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8",
			host="ec2-34-206-148-196.compute-1.amazonaws.com",
			port="5432",
			database="d2gpgbag2bgopb")
#		params = config()
	
#		conn = psycopg2.connect(**params)
		
		cur = conn.cursor() # creating cursor object

		""" insert a new player int players table """
		sql = """INSERT INTO player(id, first_name, last_name, codename) VALUES(%s,%s,%s,%s)"""
		record_to_insert = (ID, FIRST_NAME, LAST_NAME, CODENAME)

		cur.execute(sql, record_to_insert) # execute the INSERT command
		
		conn.commit() # commit the changes to the database
		
		cur.close() # close communication with the database
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


#Splash screen (default) route. Redirect to player entry screen after initializing components
@app.route("/")#allows for us to change something when a user uses one of our inputs
def splash():
	insert_player(2, "Big", "Boi", "Hulk")
	return render_template('splash.html'),{"Refresh": "3; url=./playerEntry2"}

@app.route("/playerEntry2", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
def playerEntry2():
	flash("player entry test")
	return render_template("playerEntry2.html")

@app.route("/edit", methods = ["POST", "GET"]) 
def row2():
	flash("hi " + str(request.form["player_input"]))
	iD = str(request.form.getlist["player_id"])
	codename = str(request.form.getlist["player_codename"])
	first_name = str(request.form.getlist["player_first"])
	last_name = str(request.form.getlist["player_last"])
	print(iD)
	print(codename)
	print(first_name)
	print(last_name)
	pass

if __name__ == "__main__":
	app.run(debug=True)
