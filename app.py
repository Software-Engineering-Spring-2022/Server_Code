
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify, session
# from flask_sockets import Sockets
from turbo_flask import Turbo#Used to keep the action screen dynamic

import os
import time
import socket, select
import random
import json
import threading

os.system("pip install psycopg2-binary")
os.system("pip install Flask-Session")
os.system("pip install jquery") #used in the action screen html 
os.system("pip install flask-celery")
os.system("pip install redis")
from celery import Celery
import psycopg2

# -- sample program from this video <https://youtu.be/6plVs_ytIH8>
#  --specific code was created by Matt and james.

#Global Variables
localIP     = "127.0.0.1"
localPort   = 7501
bufferSize  = 1024
i = 0
# List to store events
events = ["Start","","","",""]
numPlayers = 0
RedTeamScore = 0
BlueTeamScore = 0

# Player Object
class Player:
	def __init__(self, IDno, Code, First, Last, teamName):
		self.ID = IDno
		self.Codename = Code
		self.FirstName = First
		self.LastName = Last
		self.team = teamName
		self.Score = 0
		print("Player Created")
	def getCode(self):
		return self.Codename
	def getTeam(self):
		return self.team
	def getScore(self):
		return self.Score
	def getID(self):
		return self.ID
	def score(self):
		self.Score = self.Score+1

#An array of player objects
Players = []

#Threading utility. I believe this is superfluous in the current implementation
def make_celery(app):
	celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
	celery.conf.update(app.config)
	
	class ContextTask(celery.Task):
		def __call__(self, *args, **kwargs):
			with app.app_context():
				return self.run(*args, **kwargs)
	celery.Task = ContextTask
	return celery

#Setup of various packages
app = Flask(__name__)#makes a class for the app or program we wish to run
app.config.update(CELERY_BROKER_URL='redis://localhost:6379', CELERY_RESULT_BACKEND='redis://localhost:6379')
app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate
celery = make_celery(app)
turbo = Turbo(app)#Dynamic Page Updates

#Add a player to the database.
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
		
		print(ID)
		print(FIRST_NAME)
		print(LAST_NAME)
		print(CODENAME)
		
		#Insert a player object into the player array
		#removing this because you should only send players to action screen if they are already created
		# global Players
		# global numPlayers
		# Players.append(Player(ID, CODENAME, FIRST_NAME, LAST_NAME, team))
		# numPlayers = numPlayers+1
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()


#Searching the database to find a player.
def search_player(ID, FIRST_NAME, LAST_NAME, CODENAME, team):	# Call this to insert players into the database table player
	conn = None
	try:
		conn = psycopg2.connect( # connects to database
			user="lezbitgtjkbfrs",
			password="aa6fa77497eff9cdf22c8d618ab6277c8df71e537b9c2e46237fd3901277f7f8",
			host="ec2-34-206-148-196.compute-1.amazonaws.com",
			port="5432",
			database="d2gpgbag2bgopb")
		
		cur = conn.cursor() # creating cursor object

		""" Searching the database to find a player """
		cur.execute("SELECT first_name, last_name, codename FROM player where id="+ ID)

		#print("The number of parts: ", cur.rowcount) -- this is a print statement for debugging

		#if there is more than 0 id's in our database
		if(cur.rowcount > 0):
			#Insert a player object into the player array to get pushed to the Action screen
			global Players
			global numPlayers
			Players.append(Player(ID, CODENAME, FIRST_NAME, LAST_NAME, team))
			numPlayers = numPlayers+1

		#if there is not an id in the database
		else:
			print(ID+" was not found. Please create the player before playing the game.")
			return 0
		
		cur.close() # close communication with the database
		
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
	finally:
		if conn is not None:
			conn.close()

#UDP Listener and action screen updater
@celery.task()
def listen_to_udp():
	time.sleep(30)
	UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	UDPServerSocket.bind((localIP, localPort))
	
	global Players
	global numPlayers
	
	#UDP receiver
	while (True):
		trafficEvents = UDPServerSocket.recvfrom(bufferSize)
		#creates a message from the packet
		msg="{}".format(trafficEvents[0])
		print(msg)
		

		
		hitter = ""
		hit = ""
		BluePlayerNames = []
		RedPlayerNames = []
		Blink = []
		Blue = False
		Red = False
		
		#Create arrays containing the info to print for all players
		for item in Players:
			teamPlus = 0
			if(item.getID() == msg[2]):
				item.score()
				teamPlus = 1
				hitter = item.getCode()
			elif(item.getID() == msg[4]):
				hit = item.getCode()
			playerInfo = item.getCode() + " - " + str(item.getScore())
			if(item.getTeam() == 1):
				BluePlayerNames.append(playerInfo)
				global BlueTeamScore
				BlueTeamScore = BlueTeamScore + teamPlus
			else:
				RedPlayerNames.append(playerInfo)
				global RedTeamScore
				RedTeamScore = RedTeamScore + teamPlus
		
		#Update the array of events with the new event
		events[4]=events[3]
		events[3]=events[2]
		events[2]=events[1]
		events[1]=events[0]
		events[0]=(hitter + " hit " + hit)
		
		BluePlayerNames.insert(0, ("Team Score - " + str(BlueTeamScore)))
		RedPlayerNames.insert(0, ("Team Score - " + str(RedTeamScore)))
		
		# if (BlueTeamScore > RedTeamScore): 
			# Red = False
			# Blue = True
		# else if (BlueTeamScore < RedTeamScore):
			# Red = True
			# Blue = False
		# else: 
			# Red = False
			# Blue = False

		# Blink.insert(0, Red)
		# Blink.insert(1,Blue)
		
		#Push updates to the action screen html
		turbo.push(turbo.replace(render_template('events.html',events = events), 'EVENT'))
		# turbo.push(turbo.replace(render_template('actionScreen.html', Blink = Blink), 'TOP'))
		turbo.push(turbo.replace(render_template('red_team.html',red_team = RedPlayerNames), 'RED'))
		turbo.push(turbo.replace(render_template('blue_team.html',blue_team = BluePlayerNames), 'BLUE'))

#Traffic generator provided by Mr. Strother
@celery.task()
def traffic_generator():
	time.sleep(30)
	
	bufferSize  = 1024
	serverAddressPort   = ("127.0.0.1", 7501)


	print('this program will generate some test traffic for 2 players on the red ')
	print('team as well as 2 players on the blue team')
	print('')

	# red1 = input('Enter codename of red player 1 ==> ')
	# red2 = input('Enter codename of red player 2 ==> ')
	# blue1 = input('Enter codename of blue player 1 ==> ')
	# blue2 = input('Enter codename of blue player 2 ==> ')
	
	red1 = "John"
	red2 = "James"
	blue1 = "Matthew"
	blue2 = "Ryan"

	print('')
	# counter = input('How many events do you want ==> ')
	counter = 1000
	# Create datagram socket
	UDPClientSocketTransmit = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

	# counter number of events, random player and order
	i = 1
	while i < int(counter):
		if random.randint(1,2) == 1:
			redplayer = red1
		else:
			redplayer = red2

		if random.randint(1,2) == 1:
			blueplayer = blue1
		else: 
			blueplayer = blue2	

		# if random.randint(1,2) == 1:
			# message = redplayer + " hit " + blueplayer
		# else:
			# message = blueplayer + " hit " + redplayer
		
		# if random.randint(1,2)==1:
			# integer1=str(random.randint(1,2))
			# integer2=str(random.randint(3,4))
		# else:
			# integer1=str(random.randint(3,4))
			# integer2=str(random.randint(1,2))
		
		integer1 = random.randint(0,(numPlayers-1))
		integer2 = random.randint(0,(numPlayers-1))

		if(Players[integer1].getTeam() != Players[integer2].getTeam()):
			message = Players[integer1].getID()+":"+Players[integer2].getID()
			print(message)
			i+=1;
			UDPClientSocketTransmit.sendto(str.encode(str(message)), serverAddressPort)
		time.sleep(random.randint(1,3))
		
	print("program complete")

#Splash screen (default) route. Redirect to player entry screen after initializing components
@app.route("/")#allows for us to change something when a user uses one of our inputs
def splash():
	return render_template('splash.html'),{"Refresh": "3; url=./playerEntry2"}

#Current version of player entry screen
@app.route("/playerEntry2", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
def edit():
	if request.method == 'POST':
		
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

		#New Players
		iD_new = data.getlist("player_id_new")#the .getlist("name") method is from the flask module. changes the dict to an indexable list
		codename_new = data.getlist("player_codename_new")
		first_name_new = data.getlist("player_first_new")
		last_name_new = data.getlist("player_last_new")

		

		#Testing that data was gotten

		#using try catch in case the program breaks

		#new player
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

		#blue team	
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
					# if( search_player(iD_b[x],first_name_b[x],last_name_b[x],codename_b[x],1) == 0):
					# 	return render_template('playerEntry2.html', message='Please enter required fields')
					search_player(iD_b[x],first_name_b[x],last_name_b[x],codename_b[x],1)
				#we need to filter blank inputs so as to not fill the database with empty entries
		except:
			print("cant push blue team data, check code")
			
		#red team
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
					search_player(iD_r[x],first_name_r[x],last_name_r[x],codename_r[x],2)
				#we need to filter blank inputs so as to not fill the database with empty entries
		except:
			print("cant push red team data, check code")
		#running list of players in current game
		

		session['blue_team'] = codename_b
		session['red_team'] = codename_r
		
	return render_template("playerEntry2.html") #needs to be edited so that the user input persists

#Action screen
@app.route("/actionScreen", methods = ["GET"]) #game action screen page	
def plyr_scrn():
	
	
#This is the code which starts the UDP server and traffic generator
#It should be with the code that executes during the game
#If that code moves somewhere, please move this too
	t1 = threading.Thread(target = listen_to_udp)
	t1.start()
	t2 = threading.Thread(target = traffic_generator)
	t2.start()
	print("UDP server up and listening")
#End of UDP code
	red_team_test = [""]
	blue_team_test = [""]
	
	red_team_test.append(session.get('red_team',str))
	blue_team_test.append(session.get('blue_team',str))
	
	red_team_test.append("")
	blue_team_test.append("")
	
	print(red_team_test)
	print(blue_team_test)
	
	return render_template("actionScreen.html")

@app.route("/_event_update", methods = ["GET"]) #game action screen page	
def event_update():
	return jsonify(events)

#Run the application
if __name__ == "__main__":
	app.run(debug=True)
