# Tim Ng, Daniel Park, Will Nzeuton, Yinwei Zhang
# Team lobo2
# SoftDev
# p02
# 2024-1-09

import json
import sqlite3
import os
import os.path

import random
import string
from datetime import datetime

from auth_utils import password_hash, get_logged_in_user

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
                match_rank JSON NOT NULL,
                liked TEXT COLLATE NOCASE DEFAULT ''
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
    if(not os.path.isfile(DB_FILE)):
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
        c.execute("INSERT INTO users (name_first, name_last, hash, email, dob, profile, preferences, match_rank) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (name_first, name_last, password_hash(password)[0], email, dob, profile, preferences, match_rank))
        db.commit()
    except sqlite3.IntegrityError as e:
        print(name_first, name_last)
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
def count_users():
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT COUNT(*) FROM users")
        n = c.fetchone()[0]
        return n
    except sqlite3.IntegrityError:
        print(f"create_user: {e}")
    finally:
        c.close()

def read_profile(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT profile FROM users WHERE id = ?", (user_id,))
        profile = c.fetchone()[0]
        return json.loads(profile)
    except sqlite3.Error as e:
        print(f"read_profile: {e}")
    finally:
        c.close()


def read_prefs(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT preferences FROM users WHERE id = ?", (user_id,))
        prefs = c.fetchone()[0]
        return json.loads(prefs)
    except sqlite3.Error as e:
        print(f"read_profile: {e}")
    finally:
        c.close()

def read_ranks(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT match_rank FROM users WHERE id = ?", (user_id,))
        ranks = c.fetchone()[0]
        return json.loads(ranks)
    except sqlite3.Error as e:
        print(f"read_ranks: {e}")
    finally:
        c.close()

def read_likes(user_id):
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute("SELECT liked FROM users WHERE id = ?", (user_id,))
        likes = c.fetchone()[0]
        likes_list = likes.split(",")
        for i in range(len(likes_list)):
            user = likes_list[i]
            if user != '':
                likes_list[i] = int(user)
            else:
                likes_list.pop(i)
                i -= 1
        return likes_list
    except sqlite3.Error as e:
        print(f"read_likes: {e}")
    finally:
        c.close()

def add_like(user_id):
    logged_in_user = get_logged_in_user()[0]
    existing_likes = read_likes(user_id)
    if(logged_in_user in existing_likes):
        return None
    existing_likes.append(logged_in_user)
    new_string = ','.join([str(i) for i in existing_likes])
    db = sqlite3.connect(DB_FILE)
    try:
        c = db.cursor()
        c.execute(f"UPDATE users SET liked = ? WHERE id = ?", (new_string, user_id))
        db.commit()
    except sqlite3.Error as e:
        print(f"add_like: {e}")
    finally:
        c.close()
#----- Preset data creation -----
def fill_db(n):
    male_first_names = [
        "Yinwei", "Will", "Liam", "Tim", "Noah", "Oliver", "Elijah", "James", "William", "Benjamin", "Lucas", "Henry", "Alexander",
        "Mason", "Michael", "Ethan", "Daniel", "Jacob", "Logan", "Jack", "Aiden", "Matthew", "Joseph", "Samuel",
        "David", "Carter", "Owen", "Wyatt", "John", "Luke", "Anthony", "Dylan", "Isaac", "Grayson", "Gabriel",
        "Leo", "Julian", "Aaron", "Charles", "Christopher", "Joshua", "Andrew", "Thomas", "Nathan", "Harrison",
        "Connor", "Landon", "Zachary", "Hunter", "Isaiah", "Asher", "Caleb", "Christian", "Cameron", "Ryan",
        "Jordan", "Eli", "Adam", "Miles", "Xavier", "Colton", "Austin", "Josiah", "Dominic", "Nolan", "Robert",
        "Evan", "Ian", "Santiago", "Cooper", "Victor", "Ezekiel", "Lincoln", "Jaxon", "Luis", "Kai", "Maverick",
        "Alex", "Axel", "Jameson", "Sean", "Everett", "Blake", "Karter", "Sawyer", "Max", "Milo", "Beau",
        "Maddox", "Giovanni", "Tristan", "Elliott", "Brayden", "Cole", "Jude", "Hudson", "Bennett", "Arthur",
        "Grant", "Easton", "Finn", "Riley", "Seth", "Kingston", "Ashton", "Brock", "Jace", "Jasper", "Wesley",
        "Emmett", "Tobias", "Felix", "Camden", "Charlie", "Dawson", "Luca", "Theo", "George", "Jaxson", "Sullivan",
        "Roman", "Phoenix", "Finley", "Beckett", "Damian", "Theo", "Milo", "Knox", "Maddox", "Greyson", "Cassius",
        "Hugo", "Winston", "Zane", "Ford", "Cash", "Reed", "Easton", "Chase", "Deacon", "Tyler", "Blaine", "Axel",
        "Zander", "Griffin", "Jett", "Sterling", "Maximus", "Zion", "Joaquin", "Finnegan", "Franklin", "Lachlan",
        "Atticus", "Sawyer", "Everett", "Roman", "Sage", "Caden", "Kaius", "Dakota", "Emilio", "Kai", "River",
        "Alfred", "Thatcher", "Ronan", "Hendrix", "Harris", "Theo", "Weston", "Asher", "Alec", "Dante", "Moses",
        "Trent", "Fletcher", "Clyde", "Dawson", "Baxter", "August", "Oliver", "Cason", "Gage", "Maverick", "Ryder",
        "Malcolm", "Alvin", "Dean", "Lennox", "Odin", "Harrison", "Vance", "Brody", "Caden", "Tanner", "Westley",
        "Kellan", "Emmett", "Quentin", "Preston", "Donovan", "Ronin", "Paxton", "Briggs", "Talon", "Sonny", "Calvin"
    ]
    female_first_names = [
        "Zhang", "Nzeuton", "Ng", "Park", "Olivia", "Emma", "Ava", "Sophia", "Isabella", "Mia", "Amelia", "Harper", "Evelyn", "Abigail",
        "Ella", "Scarlett", "Grace", "Chloe", "Aria", "Zoe", "Nora", "Lily", "Avery", "Charlotte", "Elizabeth",
        "Sofia", "Victoria", "Madison", "Eleanor", "Hazel", "Luna", "Riley", "Leah", "Ellie", "Paisley", "Lillian",
        "Addison", "Willow", "Lucy", "Audrey", "Bella", "Nova", "Brooklyn", "Hannah", "Savannah", "Maya", "Skylar",
        "Layla", "Leila", "Kinsley", "Sophie", "Violet", "Claire", "Ariana", "Alice", "Camila", "Lila", "Ruby",
        "Sarah", "Kennedy", "Caroline", "Madeline", "Katherine", "Mackenzie", "Stella", "Naomi", "Sadie", "Eva",
        "Archer", "Samantha", "Genesis", "Maria", "Autumn", "Gemma", "Lydia", "Zara", "Natalie", "Rylee", "Penelope",
        "Cora", "Peyton", "Juliana", "Vivian", "Eliana", "Emilia", "Jade", "Aubrey", "Isabel", "Quinn", "Savannah",
        "Tessa", "Gianna", "Lauren", "Madelyn", "Aspen", "Summer", "Adeline", "Mila", "Ember", "Gracie", "Ivy", "Megan",
        "Alaina", "Delilah", "Mariah", "Jasmine", "Norah", "Dakota", "Alexa", "Riley", "Kylie", "Cecilia", "Sienna", "Sage",
        "Serenity", "Summer", "Lilyana", "Mckenna", "Payton", "Aubree", "Reagan", "Caitlyn", "Hadley", "Brianna", "Autumn",
        "Blake", "Lola", "Roxanne", "Jocelyn", "Bianca", "Sabrina", "Delaney", "Cameron", "Brooke", "Marley", "Teagan", "Sloane",
        "Ellis", "Kaitlyn", "Kendall", "Juliette", "Maggie", "Leah", "Rory", "Ashley", "Aiden", "Tatum", "Addyson", "Jordan", "Piper",
        "Megan", "Alicia", "Paige", "Valeria", "Lia", "Carmen", "Finley", "Chloe", "Amaya", "Scarlet", "Tatum", "Avery", "Sophia", "Megan",
        "Sophie", "Vivienne", "Diana", "Phoebe", "Harleigh", "Rosalie", "Jolie", "Genevieve", "Caitlin", "Hope", "Sierra", "Paisley", "Emersyn",
        "Abby", "Rosie", "Molly", "Nina", "Lana", "Lilah", "Brynlee", "Hayden", "Tori", "Brynlee", "Ainsley", "Elsa", "Allison", "Addison", "Izzy",
        "Opal", "Nellie", "Juniper", "Athena", "Finley", "Lola", "Carly", "Alyssa", "Mira", "Lark", "Zoey", "Mariana", "Eden", "Fiona"
    ]
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "García", "Rodríguez", "Martínez",
        "Hernández", "Lopez", "González", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "White", "Harris", "Sánchez", "Clark", "Ramírez", "Lewis", "Roberts", "Gómez", "Hall", "Young",
        "King", "Scott", "Green", "Adams", "Baker", "Nelson", "Carter", "Mitchell", "Perez", "Robinson", "Walker", "Evans",
        "Torres", "Collins", "Edwards", "Stewart", "Morris", "Murphy", "Rivera", "Cook", "Rogers", "Gutierrez", "Ortiz",
        "Morgan", "Cooper", "Reyes", "Jenkins", "Parker", "Kim", "Bell", "Wright", "Chavez", "Diaz", "Hayes", "Myers",
        "Ford", "Hughes", "Washington", "Butler", "Simmons", "Foster", "Patterson", "Gray", "James", "Dixon", "Hansen",
        "Hernandez", "Graham", "Kelly", "Bowman", "Webb", "Ryan", "Williamson", "Campbell", "Bennett", "Bryant", "Harrison",
        "Diaz", "Gibson", "Mendoza", "Richards", "Williamson", "Carson", "Riley", "Warren", "Chang", "Norris", "Sullivan",
        "Bishop", "Shaw", "Davidson", "Alexander", "Cameron", "Palmer", "Mills", "Gibson", "Hoffman", "Cunningham", "Black",
        "Snyder", "Johnston", "Dean", "Chavez", "Meyer", "Brock", "Ferguson", "Mason", "Ryan", "Tucker", "Arnold", "Freeman"
    ]

    for i in range(n):
        chosen_gender = random.randint(0, 1)
        chosen_name = None

        if(chosen_gender == 0):
            chosen_name = random.choice(male_first_names)
        if(chosen_gender == 1):
            chosen_name = random.choice(female_first_names)

        chosen_name += " " + random.choice(last_names)

        first_name, last_name = chosen_name.split(' ')

        dob_year = random.randint(2007, 2010)
        dob_month = random.randint(1, 12)
        dob_day = random.randint(1, 28)

        dob = datetime(dob_year, dob_month, dob_day)

        hash = "hash"
        email = first_name.lower() + str(i) + "@gmail.com"
        profile = {
            "height": random.randint(25, 47) + random.randint(25, 47),
            "gender": random.choice([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]),
            "grade": random.randint(9, 12),
            "location": random.choice(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"]),
            "interests": random.sample(["Sports", "Music", "Art", "Tech", "Gaming", "Reading", "Traveling"], k=random.randint(2, 5)),
            "bio": " ".join(random.choices(string.ascii_letters + " ", k=50)).strip(),
            "picture": f"/images/user_{random.randint(1, 1000)}.jpg"
        }
        prefs = {
            "grade": {
                "pref": random.sample(range(9, 13), k=random.randint(1, 4)),
                "required": random.choice([True, False, False, False])
            },
            "gender": {
                "pref": random.sample(range(0, 3), k=random.randint(1, 3)),
                "required": random.choice([True, False, False, False])
            },
            "location": {
                "pref": random.sample(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"], k=random.randint(1, 5)),
                "required": random.choice([True, False, False, False])
            },
            "height": {
                "pref": list(range(random.randint(60, 68), random.randint(68, 84))),
                "required": random.choice([True, False, False, False])
            },
            "interests": {
                "pref": random.sample(["Sports", "Music", "Art", "Tech", "Gaming", "Reading", "Traveling"], k=random.randint(3, 5)),
                "required": random.choice([False])
            }
        }
        match_rank = {}
        create_user(first_name, last_name, "password", email, dob, json.dumps(profile), json.dumps(prefs), json.dumps(match_rank))
