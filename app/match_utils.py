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

def compatibility_score(user1_id, user2_id):
    score1 = pref_match(user1_id, user2_id)
    score2 = pref_match(user2_id, user1_id)
    total_score = score1 + score2

    print(f"Compatibility between {user1_id} and {user2_id}: {total_score} (Score1: {score1}, Score2: {score2})")
    return total_score


def create_match_rank(user_id):
    ranks = {}
    for other_user_id in range(1, count_users() + 1):
        if user_id != other_user_id:  # Skip self
            score = compatibility_score(user_id, other_user_id)
            if score > 0:  # Only store positive scores
                ranks[other_user_id] = score

    match_rank = dict(sorted(ranks.items(), key=lambda item: item[1], reverse=True))
    update_user(user_id, "match_rank", json.dumps(match_rank))
    print(f"Match ranks for user {user_id}: {match_rank}")


def update_match_ranks():
    for user in range(1, count_users() + 1):
        create_match_rank(user)

def select_matches(user_id):
    likes = read_likes(user_id)
    print(f"Likes for user {user_id}: {likes}")

    ranks = read_ranks(user_id)
    print(f"Ranks for user {user_id}: {ranks}")

    matches = [key for key, value in ranks.items() if value > 0 and key not in likes]
    print(f"Matches for user {user_id}: {matches}")

    return likes + matches

