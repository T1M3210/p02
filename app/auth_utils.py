# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

import os
import sqlite3
from flask import session
import bcrypt

DB_FILE = os.path.join(os.path.dirname(__file__), "../xase.db")

def is_valid_username(username):
    return not any(c in ' ~!@#$%^&*()`\\\'\";:[]{«»‘“}|,<>/?' for c in username)

def email_password_match(email, password):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT hash FROM users WHERE email = ?", (email,))
        stored_pw = c.fetchone()[0]
        db.commit()
    except sqlite3.Error as e:
        print(f"email_password_math: {e}")
    finally:
        c.close()

    return check_password(stored_pw, password)

def user_exists(value, type):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute(f"SELECT 1 FROM users WHERE {type} = ?", (value,))
        result = c.fetchone()
        print(f"{result is not None}: {value}")
        return result is not None
    except sqlite3.Error as e:
        print(f"user_exists: {e}")
    finally:
        c.close()

#Retrieve user id by username or email
def user_column_to_id(value, type):
    res = -1
    if type not in ['username', 'email']:
        raise KeyError(f"{type} is not a valid column type of user_column_to_id")
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute(f"SELECT id FROM users WHERE {type} = ?", (value,))
        res = c.fetchone()[0]
        db.commit()
    except sqlite3.Error as e:
        print(f"user_column_to_id: {e}")
    finally:
        c.close()
        return res

def is_logged_in():
    return 'user' in session

def get_logged_in_user():
    return session.get('user', None)

def password_hash(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed, salt

def check_password(pw_hash, password):
    return bcrypt.checkpw(password.encode('utf-8'), pw_hash)
