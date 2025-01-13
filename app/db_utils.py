# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

import json
import sqlite3
import os

import random
import string
from datetime import datetime

from auth_utils import password_hash
#Establish database file path
DB_FILE = os.path.join(os.path.dirname(__file__), "../xase.db")

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

# --------------- Operational Funcprofiletions ---------------

# ----- users Functions -----

def create_user(name_first, name_last, password, email, dob, profile, preferences, match_rank):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("INSERT INTO users (name_first, name_list, hash, email, dob, profile, preferences, match_rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name_first, name_last, password, email, dob, profile, preferences, match_rank))
        db.commit()
    except sqlite3.IntegrityError:
        print(f"create_user: {e}")
    finally:
        c.close()

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

#----- Preset data creation -----
def fill_db(n):
    male_first_names = ('Topher', 'Topher', 'Topher', 'Topher', 'John', 'Daniel', 'Tasnim', 'Tahmim', 'Mark', 'Kenneth', 'Dave', 'Bob', 'Will', 'Tim', 'Jake', 'Dexter', 'Jacob', 'Joe', 'David', 'Aiden', 'James', 'Michael', 'Henry', 'Ryan') 
    female_first_names = ('Emily', 'Anne', 'Hannah', 'Michelle', 'Danielle', 'Rebecca', 'Abby', 'Zoey', 'Andrea', 'Grace', 'Stella' , 'Vivienne', 'Sandra', 'Melanie', 'Melody', 'Taylor', 'Catherine')
    last_names = ('Mykolyk', 'Mykolyk', 'Mykolyk', 'Mykolyk', 'Mykolyk', 'Williams', 'Smith', 'Ng', 'Park', 'Kim', 'Zhang', 'Zhou', 'Nzeuton', 'James', 'Garcia', 'Nzeuton', 'Islam', 'Gabai', 'Hassan', 'Chen', 'Chan', 'Rahman', 'Singh', 'Marcus', 'Patel', 'Nguyen', 'Johnson', 'Dickinson', 'Richards', 'Philips', 'Cartier', 'Dior', 'Bird')

    for i in range(n):
        chosen_gender = random.randint(0, 1)
        chosen_name = None

        if(chosen_gender == 0):
            chosen_name = random.choice(male_first_names)
        if(chosen_gender == 1):
            chosen_name = random.choice(female_first_names)

        chosen_name += " " + random.choice(last_names)

        first_name, last_name = chosen_name.split(' ')

        print(chosen_name)

        dob_year = random.randint(2007, 2010)
        dob_month = random.randint(1, 12)
        dob_day = random.randint(1, 29)

        dob = datetime(dob_year, dob_month, dob_day)

        print(dob)

        hash = "hash"
        email = first_name.lower() + str(i) + "@gmail.com"
        profile = {
            "height": random.randint(150, 200), 
            "gender": random.randint(0, 2), 
            "grade": random.randint(9, 12),
            "location": random.choice(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]),
            "interests": random.sample(["Sports", "Music", "Art", "Tech", "Gaming", "Reading", "Traveling"], k=random.randint(2, 5)),
            "bio": " ".join(random.choices(string.ascii_letters + " ", k=50)).strip(), 
            "picture": f"/images/user_{random.randint(1, 1000)}.jpg" 
        }
        prefs = {
            "grade": {
                "pref": random.sample(range(9, 13), k=random.randint(1, 4)), 
                "required": random.choice([True, False])
            },
            "gender": {
                "pref": random.sample(range(0, 3), k=random.randint(1, 3)), 
                "required": random.choice([True, False])
            },
            "location": {
                "pref": random.sample(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"], k=random.randint(1, 5)),
                "required": random.choice([True, False])
            },
            "height": {
                "pref": (random.randint(48, 60), random.randint(61, 78)),  
                "required": random.choice([True, False])
            },
            "interests": {
                "pref": random.sample(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"], k=random.randint(1, 3)),  
                "required": random.choice([True, False])
            }
        }
        match_rank = {
            f"user_{i}": random.randint(50, 100)  # Compatibility scores
            for i in range(1, random.randint(5, 15))  # Random number of matches
        }
        print(profile)
        print(prefs)

        create_user(first_name, last_name, "password", email, dob, profile, prefs, match_rank)



