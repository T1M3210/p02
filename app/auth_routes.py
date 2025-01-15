# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

from flask import render_template, request, redirect, url_for, flash, session

from auth_utils import *
from db_utils import *
from match_utils import *

def init_auth_routes(app):
    @app.route("/login", methods=['GET', 'POST'])
    def login():
        is_logging = request.form
        if(is_logging):
                email = request.form['email']
                password = request.form['password']

                if(user_exists(email, "email")):
                        if(email_password_match(email, password)):
                                    session['user'] = read_user(user_column_to_id(email, "email"))
                                    if len(read_ranks(session['user'][0])) ==  0:
                                           return redirect(url_for('onboard'))
                                    else:
                                           update_match_ranks()
                                    return redirect(url_for('home'))
                        else:
                                flash("Incorrect password")
                else:
                        flash("Could not find a user with that email")
        return render_template('login.html')

    @app.route("/signup", methods=['GET', 'POST'])
    def signup():
        is_signing = request.form
        if(is_signing):
                name_first = request.form['name_first']
                name_last = request.form['name_last']
                dob = request.form['dob']
                email = request.form['email']
                password = request.form['password']
                confirm_password = request.form['confirm_password']

                is_error = False

                if(user_exists(email, "email")):
                        flash("An account already exists with that email")
                        is_error = True

                if(password != confirm_password):
                        flash("Passwords don't match")
                        is_error = True

                if(not is_error):
                        create_user(name_first, name_last, password, email, dob, json.dumps({}), json.dumps({}), json.dumps({}))
                        flash("Successfully created account! Redirected to onboarding")
                        session['user'] = read_user(user_column_to_id(email, "email"))
                        return redirect(url_for('onboard'))
                else:
                        return render_template('signup.html')
        else:
                return render_template("signup.html")

    @app.route("/logout", methods=['GET', 'POST'])
    def logout():
        if(is_logged_in()):
            session.pop('user')
        return redirect(url_for('home'))
