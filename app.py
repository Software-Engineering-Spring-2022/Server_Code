
from flask import Flask, render_template, request, flash, redirect, url_for

import os
import time
import socket
import random
import json

os.system("pip install psycopg2-binary")
import psycopg2
# -- sample program from this video <https://youtu.be/6plVs_ytIH8>
#  --specific code was created by Matt and james.

app = Flask(__name__)#makes a class for the app or program we wish to run
app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate
i = 0
# List to store events
events = [""]

def insert_player(ID, FIRST_NAME, LAST_NAME, CODENAME):	# Call this to insert players into the database table player
	conn = None
	try:
		conn = psycopg2.connect( # connects to database
			user="lezbitgtjkbfrs",
			password="aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8",
			host="ec2-34-206-148-196.compute-1.amazonaws.com",
			port="5432",
			database="d2gpgbag2bgopb")
		
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
#this class will allows other methods to access the current game players
# class Players:
# 	@classmethod
# 	def __init__(self,red,blue):
# 		Players.curr_red_plyrs = red
# 		Players.curr_blue_plyrs = blue			
# 	@classmethod
# 	def _get_red(self):
# 		print(Players.curr_red_plyrs)
# 		return self.curr_red_plyrs
# 	@classmethod
# 	def _get_blue(self):
		
# 		return self.curr_blue_plyrs
	

#Splash screen (default) route. Redirect to player entry screen after initializing components
@app.route("/")#allows for us to change something when a user uses one of our inputs
def splash():
	return render_template('splash.html'),{"Refresh": "3; url=./playerEntry2"}

@app.route("/playerEntry2", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
def edit():
	if request.method == "POST":

		global red
		global blue

		#this method routes to the template for player entry
		#it will allow the user to input data in the text boxes provided 
		#when the user presses submit it will send the data to app.py
		#the data will then be entered in a for loop sequentially view the 
		#DB teams insert_player method

		#data lists instantiated
		#New Players
		iD_new = []
		codename_new=[]
		first_name_new=[]
		last_name_new=[]

		#Blue Team
		iD_b = []
		codename_b=[]
		first_name_b=[]
		last_name_b=[]

		#Red Team
		iD_r = []
		codename_r=[]
		first_name_r=[]
		last_name_r=[]

		#request data from the 'edit' form (check <form action="{{ url_for("edit")}}" ... in the html)
		data = request.form
		#New Players
		iD_new = data.getlist("player_id_new")#the .getlist("name") method is from the flask module. changes the dict to an indexable list
		codename_new = data.getlist("player_codename_new")
		first_name_new = data.getlist("player_first_new")
		last_name_new = data.getlist("player_last_new")

		#Blue Team
		iD_b = data.getlist("player_id_b")#the .getlist("name") method is from the flask module. changes the dict to an indexable list
		codename_b = data.getlist("player_codename_b")
		first_name_b = data.getlist("player_first_b")
		last_name_b = data.getlist("player_last_b")

		

		#Red Team
		iD_r = data.getlist("player_id_r")#the .getlist("name") method is from the flask module. changes the dict to an indexable list
		codename_r = data.getlist("player_codename_r")
		first_name_r = data.getlist("player_first_r")
		last_name_r = data.getlist("player_last_r")
		

		#running list of players in current game
		
		
		#using try catch in case the program breaks
		try:
			
			for x in range(len(iD_new)): #there always be as many ID's as players				
				if(iD_new[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(first_name_new[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(last_name_new[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(codename_new[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				else:
					insert_player(iD_new[x],first_name_new[x],last_name_new[x],codename_new[x])
				#we need to filter blank inputs so as to not fill the database with empty entries
		except:
			print("cant push new player data, check code")
			
		try:
			
			for x in range(len(iD_b)): #there always be as many ID's as players				
				if(iD_b[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(first_name_b[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(last_name_b[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(codename_b[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				else:
					insert_player(iD_b[x],first_name_b[x],last_name_b[x],codename_b[x])
				#we need to filter blank inputs so as to not fill the database with empty entries
		except:
			print("cant push blue team data, check code")
			
		try:
			
			for x in range(len(iD_r)): #there always be as many ID's as players				
				if(iD_r[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(first_name_r[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(last_name_r[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				elif(codename_r[x] == ''):
					print("Skipping this line because the entire line was not filled out.")
				else:
					insert_player(iD_r[x],first_name_r[x],last_name_r[x],codename_r[x])
				#we need to filter blank inputs so as to not fill the database with empty entries
		except:
			print("cant push red team data, check code")
			
		if(iD_r[0] == ''):
			print("skip")
			red = "error"
			blue = "error"
		else:
			red = codename_r
			blue = codename_b

			 

	return render_template("playerEntry2.html") #needs to be edited so that the user input persists

@app.route("/playerReg", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
def regi():
	#need a method for player registration for later sprint
	#need html as well
	#needs to be able to generate IDS and submit players 
	pass

@app.route("/actionScreen", methods = ["GET"]) #game action screen page
"""
def server():
	localIP     = "127.0.0.1"
	localPort   = 7501
	bufferSize  = 1024
	msgFromServer       = "Hello UDP Client"
	bytesToSend         = str.encode(msgFromServer)
	# Create a datagram socket
	UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	# Bind to address and ip
	UDPServerSocket.bind((localIP, localPort))

	print("UDP server up and listening")
	pass
"""
def plyr_scrn():
	#calls the Players class. it is a class method, which may need to be changed in the future
	try:
		red_team = ["no players entered"]
		blue_team = ["no players entered"]
		"""
		out_file = open("current_players.json", "w")

		dictA = {

			"red_team" : 0,
			"blue_team" : 0
		}

		json.dump(dictA,out_file)

		dictA["red_team"] = red
		dictA["blue_team"] = blue

		x = json.dump(dictA,out_file)
		print(x)
		out_file.close()
		"""
	except:
		red_team = ["no players entered"] #in case one side isnt entered
		blue_team = ["no players entered"]
		
	return render_template("actionScreen.html", red_team = red_team,blue_team = blue_team,events = events)
"""
def get_next_event():
	# Listen for incoming datagrams
	bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
	message = bytesAddressPair[0]
	address = bytesAddressPair[1]
	clientMsg = "Message from Client:{}".format(message)
	clientIP  = "Client IP Address:{}".format(address)

	print(clientMsg)
	print(clientIP)

	# Sending a reply to client
	UDPServerSocket.sendto(bytesToSend, address)
"""
if __name__ == "__main__":
	app.run(debug=True)
	
	
	
	
 
