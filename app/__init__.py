# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

BASE_DIR = os.path.abspath(os.path.dirname(__file__)) #link xase.db
DB_PATH = os.path.join(BASE_DIR, 'xase.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return render_template('index.html')

def
if __name__ == "__main__":
    app.debug = True
    app.run()
