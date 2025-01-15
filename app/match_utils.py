import json

from db_utils import *

def pref_match(user1_id, user2_id):
    score = 0
    user1_pref = read_prefs(user1_id)
    user2_prof = read_profile(user2_id)
    # Check requirements
    for data in user1_pref.keys():
        # Preference is always a list
        preference = user1_pref[data]["pref"]
        required = user1_pref[data]["required"]
        profile = user2_prof[data]
        if required and profile not in preference:
            return -1000000
        if profile in preference:
            score += 1
        elif data == "interests":
            for i in preference:
                if i in profile:
                    score += 1
    return score

def compatibility_score(user1, user2):
    return pref_match(user1, user2) + pref_match(user2, user1)

def create_match_rank(n):
    ranks = {}
    for user2 in range(1, count_users() + 1):
        if(n != user2):
            ranks[user2] = compatibility_score(n, user2)
    match_rank = dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))
    update_user(n, "match_rank", json.dumps(match_rank))

def update_match_ranks():
    for user in range(1, count_users() + 1):
        create_match_rank(user)

def find_liked(user_id):
    users = []
    for user in range(1, count_users() + 1):
        if(user_id in read_likes(user)):
            users.append(user)
    print(f"People who like {user_id}: {users}")
    return users

def select_matches(user_id):
    likes = find_liked(user_id)
    matches = [key for key, value in read_ranks(user_id).items() if value > 0 and value not in likes]
    return likes + matches