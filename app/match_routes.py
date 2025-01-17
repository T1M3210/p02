import json

from db_utils import *
from auth_utils import *
from match_utils import *

from flask import render_template, redirect, url_for

def init_match_routes(app):
    @app.route("/matches")
    def matches():
        user_id = get_logged_in_user()[0]
        user_ids = select_matches(user_id)

        print(f"User {user_id} potential matches: {user_ids}")  # Debug log

        users = [read_user(id) for id in user_ids]
        processed_users = []
        for user in users:
            user_list = list(user)
            user_list[6] = json.loads(user_list[6])  # Parse profile JSON
            processed_users.append(user_list)

        return render_template("matches.html", users=processed_users)



    @app.route("/like/<int:user_id>")
    def like(user_id):
        add_like(user_id)
        if(user_id in find_liked(get_logged_in_user()[0])):
            print("MATCH MATCH MATCH MATCH MATCH")
        return redirect(url_for('matches'))
