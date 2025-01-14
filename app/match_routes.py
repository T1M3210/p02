import json

from db_utils import *

from flask import render_template

def register_routes(app):
    @app.route("/matches")
    def matches():
        ranks = read_ranks(1)
        print(ranks)
        users = [read_user(id) for id in list(ranks.keys())[:10]]
        processed_users = []
        for user in users:
            user_list = list(user)
            profile = user_list[6]
            js = json.loads(profile)
            user_list[6] = js
            
            processed_users.append(user_list)
        return render_template('matches.html', users=processed_users)