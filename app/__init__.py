# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

from db_utils import *
from match_utils import *
from auth_utils import *

from match_routes import init_match_routes
from auth_routes import init_auth_routes

db = DB_FILE = os.path.join(os.path.dirname(__file__), "../xase.db")

setup_db()

zoey_profile = {
    "height": 64,
	"gender": 1,
	"grade": 12,
	"location": "Manhattan",
	"interests": ["Music", "Reading", "Money"],
	"bio": "gay people are still people",
	"picture": "/zmail/0.jpg"
}

zoey_preferences = {
    "grade": {
            "pref": [12],
            "required": True
    },
    "gender": {
            "pref": [0,1,2],
            "required": False
    },
    "location": {
            "pref": ["Manhattan"],
            "required": False
    },
    "height": {
        "pref": [i for i in range(66, 72)],
        "required": True
    },
    "interests": {
        "pref": ["Music", "Having fun"],
        "required": False
    }
}

create_user("Zoey", "Marcus", "password", "zmail@gmail.com", "8/28/2007", json.dumps(zoey_profile), json.dumps(zoey_preferences), json.dumps({}))

fill_db(100)

create_match_rank(1)

init_auth_routes(app)
init_match_routes(app)

update_match_ranks()

@app.route("/")
def home():
    return render_template('index.html', logged_in = is_logged_in(), user = get_logged_in_user())

@app.route("/onboard")
def onboard():
    return render_template('onboarding.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
