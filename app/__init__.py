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

setup_db()
fill_db(5)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/onboard")
def onboard():
    return render_template('onboarding.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get_by_username(username)
        if user and user.verify_password(user.password_hash, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password.", "danger")
    return render_template('login.html')

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/profile")
def home():
    return render_template('profile.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
