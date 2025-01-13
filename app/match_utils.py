from db_utils import read_profile, read_prefs

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
            return -1
        if profile in preference:
            score += 1
    return score


def compatiblity_score(user1, user2):
    return pref_match(user1, user2) + pref_match(user2, user1)
