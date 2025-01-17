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

init_auth_routes(app)
init_match_routes(app)

#update_match_ranks()

@app.route("/")
def home():
    return render_template('index.html', logged_in = is_logged_in(), user = get_logged_in_user())

@app.route("/onboarding", methods=["POST"])
def onboarding():
    # Save profile and preferences
    user_id = get_logged_in_user()[0]
    profile = request.form.get("profile")
    preferences = request.form.get("preferences")
    
    update_user(user_id, "profile", profile)
    update_user(user_id, "preferences", preferences)
    
    # Update match ranks
    create_match_rank(user_id)

    return redirect(url_for("profile"))


@app.route("/profile")
def profile():
    if not is_logged_in():
        return render_template("profile.html", guest=True)
    
    user = get_logged_in_user()

  
    profile = json.loads(user[6]) if user[6] else {}
    preferences = json.loads(user[7]) if user[7] else {}

    user_data = {
        "name_first": user[1],
        "name_last": user[2],
        "profile": profile,
        "preferences": {
            "grades": preferences.get("grades", []),  
            "genders": preferences.get("genders", []),  
        }
    }

    return render_template("profile.html", guest=False, user=user_data)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if not is_logged_in():
        return redirect(url_for("login"))

    user_id = get_logged_in_user()[0]

    if request.method == "POST":
        grade = request.form.get("grade")
        gender = request.form.get("gender")
        interests = request.form.getlist("interests")
        bio = request.form.get("bio")

        preferred_grades = request.form.getlist("preferred_grades")
        preferred_genders = request.form.getlist("preferred_genders")

        if not grade or not gender or not bio:
            flash("All fields must be filled out.")
            return redirect(url_for("edit_profile"))

        profile = { # Prepare profile and preferences for saving
            "grade": grade,
            "gender": gender,
            "interests": interests,
            "bio": bio,
        }
        preferences = {
            "grades": preferred_grades,
            "genders": preferred_genders,
        }

        try:
            update_user(user_id, "profile", json.dumps(profile))
            update_user(user_id, "preferences", json.dumps(preferences))

            updated_user = read_user(user_id)
            session['user'] = updated_user

            flash("Profile updated successfully!")
        except Exception as e:
            print("Error updating profile:", e)
            flash("Failed to update profile. Please try again.")

        return redirect(url_for("profile"))

    user = get_logged_in_user()
    user_data = {
        "profile": json.loads(user[6]) if user[6] else {},
        "preferences": json.loads(user[7]) if user[7] else {},
    }

    return render_template("edit_profile.html", user=user_data)



if __name__ == "__main__":
    app.debug = True
    app.run()
