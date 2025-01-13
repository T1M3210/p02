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

if __name__ == "__main__":
    app.debug = True
    app.run()
