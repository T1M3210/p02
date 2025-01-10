# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

import json
import sqlite3
import os
from .auth import password_hash, user_exists
#Establish database file path
DB_FILE = os.path.join(os.path.dirname(__file__), "../db.db")

# --------------- Initializing functions ---------------
def create_tables(db):
    try:
        c = db.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name_first TEXT NOT NULL COLLATE NOCASE,
                name_last TEXT NOT NULL COLLATE NOCASE,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                hash TEXT NOT NULL,
                dob DATE NOT NULL,
                profile JSON NOT NULL,
                preferences JSON NOT NULL,
                match_rank JSON NOT NULL
            );
            ''')
        db.commit()
    except sqlite3.Error as e:
        print(f"create_table: {e}")
    finally:
        c.close()

def drop_tables(db):
    try:
        c = db.cursor()
        c.execute("DROP TABLE IF EXISTS users")
        db.commit()
    except sqlite3.Error as e:
        print(f"drop_tables: {e}")
    finally:
        c.close()

def setup_db():
    db = sqlite3.connect(DB_FILE)
    drop_tables(db)
    create_tables(db)
    db.commit()
    db.close()

# --------------- Operational Functions ---------------

# ----- users Functions -----

def create_user(name_first, name_last, password, email, dob, profile, preferences, match_rank):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("INSERT INTO users (name_first, name_list, hash, email, dob, profile, preferences, match_rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name_first, name_last, password_hash(password)[0], email, dob, profile, preferences, match_rank))
        db.commit()
    except sqlite3.IntegrityError:
        print(f"create_user: {e}")
        c.close()
        finally:

def read_user(id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT * FROM users WHERE id = ?", (id,))
        user = c.fetchone()
    except sqlite3.Error as e:
        print(f"fetch_user: {e}")
    finally:
        c.close()
        return user

def update_user(id, type, new_value):
    #sql sanitation (sanitization?)
    if type not in ['name_first', 'name_last', 'password', 'email', 'dob', 'profile', 'preferences', 'match_rank']:
        print("Invalid column type")
    else:
        db = sqlite3.connect(DB_FILE)
        try:
            c = db.cursor()
            c.execute(f"UPDATE users SET {type} = ? WHERE id = ?", (new_value, id))
            db.commit()
        except sqlite3.Error as e:
            print(f"update_user: {e}")
        finally:
            c.close()

def delete_user(id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("DELETE FROM users WHERE id = ?", (id,))
        db.commit()
    except sqlite3.Error as e:
        print(f"delete_user: {e}")
    finally:
        c.close()

#----- Matching Functions -----

def read_profile(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT profile FROM users WHERE id = ?", (id,))
        profile = c.fetchone()
    except sqlite3.Error as e:
        print(f"read_profile: {e}")
    finally:
        c.close()
        return json.loads(profile)

def read_prefs(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT preferences FROM users WHERE id = ?", (id,))
        prefs = c.fetchone()
    except sqlite3.Error as e:
        print(f"read_profile: {e}")
    finally:
        c.close()
        return json.loads(prefs)
