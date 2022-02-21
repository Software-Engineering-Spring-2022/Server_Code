# # Player entry class v1
# # Date: 2.20.22 
# # Desc: This class will allow the user to input their id
#         which will then be checked against the DB. if the id
#         exists in the DB the players codename will be added to
#         a static list of each team. if the id is not found the 
#         user will be sent to another screen to enter in their 
#         information which will then be added to the list for 
#         their team. 
#   Authors: Gavin Tomlinson, Julio Bonilla,Ryan Drake
from flask import Flask, render_template, request, flash
import os
class playerEnt:

    def __init__(self,app_name):
        print("in class playerEnt")
        self.app = app_name
        

    def plyr_sc1(self):
        app = self.app
        app.secret_key = "manbearpig_MUDMAN888" #required for flask to operate
        app.debug = True
        
        print("in method plyr_scr1")
        @app.route("/playerEntry2", methods = ["POST", "GET"]) #player entry route to the player entry form in the html
        def playerEntry2():
            flash("player entry test")
            return render_template("playerEntry2.html")

        @app.route("/edit", methods = ["POST", "GET"]) 
        def edit():
            flash("hi " + str(request.form["player_input"]))
            id = str(request.form["player_input"])
            print(id)
            return render_template("playerEntry2.html")