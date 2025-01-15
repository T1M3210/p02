import json

from db_utils import *
from auth_utils import *

from flask import render_template, redirect, url_for

def init_match_routes(app):
    @app.route("/matches")
    def matches():
        ranks = read_ranks(get_logged_in_user()[0])
        if len(read_ranks(session['user'][0])) ==  0:
            return redirect(url_for('onboard'))
        users = [read_user(id) for id in list(ranks.keys())[:10]]
        processed_users = []
        for user in users:
            user_list = list(user)
            profile = user_list[6]
            js = json.loads(profile)
            user_list[6] = js

            processed_users.append(user_list)
        return render_template('matches.html', users=processed_users)

    @app.route("/like/<int:user_id>")
    def like(user_id):
        add_like(user_id)
        print(read_likes(user_id))
        return redirect(url_for('matches'))
