# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

from flask import render_template, request, redirect, url_for, flash, session

from auth_utils import *

from __init__ import app

@app.route("/login", methods=['GET', 'POST'])
def login():
    is_logging = request.form
    if(is_logging):
            email = request.form['email']
            password = request.form['password']

            if(auth.user_exists(email, "email")):
                    if(auth.email_password_match(email, password)):
                                session['user'] = database.read_user(auth.user_column_to_id(email, "email"))
                                return redirect(url_for('matches'))
                    else:
                            flash("Incorrect password")
            else:
                    flash("Could not find a user with that email")
            return render_template('login.html')
    else:
            return render_template("login.html")

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    is_signing = request.form
    if(is_signing):
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            is_error = False

            if(not auth.is_valid_username(username)):
                    flash("Username shouldn't contain spaces or special characters")
                    is_error = True

            if(auth.user_exists(username, "username")):
                    flash("An account already exists with that username")
                    is_error = True

            if(auth.user_exists(email, "email")):
                    flash("An account already exists with that email")
                    is_error = True

            if(password != confirm_password):
                    flash("Passwords don't match")
                    is_error = True

            if(not is_error):
                    database.create_user(username, email, password)
                    flash("Succesfully created account! Redirected to login")
                    return redirect(url_for('login'))
            else:
                    return render_template('signup.html')
    else:
            return render_template("signup.html")

@app.route("/logout", methods=['GET', 'POST'])
def logout():
	if(auth.is_logged_in()):
		session.pop('user')
	return redirect(url_for('home'))
