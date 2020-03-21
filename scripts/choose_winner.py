# This function chooses the winning artwork at the end of a week,
# based on the engagement it recieved
# It is called by the main_mint.py function

# It recieves the week as input, and uses that
# to get the appropriate tweets, checks their engagement, and
# decides the winner

# Imports
import os
import time
import argparse
from twython import Twython
from create_db import Artwork, Session

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

# Get env
TWITTER_APP_KEY = os.getenv('TWITTER_APP_KEY')
TWITTER_APP_KEY_SECRET = os.getenv('TWITTER_APP_KEY_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
SCREEN_NAME=os.getenv('SCREEN_NAME')

# Create a Twython instance
t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

# A function that returns the keys (singular or multiple) have the
# highest value
def keyswithmaxval(d):
    # Get the max value
    v=list(d.values())
    max_v = max(v)
    # Get the keys that have that max value
    k=list(d.keys())
    max_keys = []
    for i in range(len (k)):
        if d[k[i]] == max_v:
            max_keys.append(k[i])
    return max_keys

def main(week):
    # Get ids from DB
    session = Session()
    ids_list = [id[0] for id in session.query(Artwork.id).filter_by(week = week ).all()]
    ids_list.sort()

    # Get the the twitter_ids based on the DB ids
    twt_id_str_dic = {}
    for id in ids_list:
        twt_id_str_dic[id] = session.query(Artwork.twitter_id_str).filter_by(id = id).first()[0]

    favorites_dic = {}
    RTs_dic = {}

    # Query twitter for the timeline of our twitter account
    timeline = t.get_user_timeline(screen_name = SCREEN_NAME )

    # Get the favorites and RTs from the tweets
    success = [False for i in range(5)]
    for i,id in enumerate(ids_list):
        twt_id_str = twt_id_str_dic[id]
        for tweet in timeline:
            if tweet['id_str'] == twt_id_str:
                # Record the number of favorites and RTs
                favorites_dic[id] = tweet['favorite_count']
                RTs_dic[id] = tweet['retweet_count']
                success[i] = True
                break

    # Get the key with most likes
    max_favorites_keys = keyswithmaxval(favorites_dic)

    # If there is a tie, get RTs
    if len(max_favorites_keys) >1:
        # Get RTs
        RTs_of_max_favorites = { key: RTs_dic[key] for key in max_favorites_keys }
        # Get the max
        max_RTs_keys = keyswithmaxval(RTs_of_max_favorites)
        # If theres another tie
        if len(max_RTs_keys) >1:
            # Choose the biggest key, as it was tweeted last (TIE BREAKER)
            winner = max(max_RTs_keys)
        # Winner tied likes but most RTs
        else:
            winner = max_RTs_keys[0]
    # Winner had most likes
    else:
        winner = max_favorites_keys[0]

    # Update the db with the favs and RTs
    for id in ids_list:
        session = Session()
        u = session.query(Artwork).get(id)
        u.favorites = favorites_dic[id]
        u.RTs = RTs_dic[id]
        session.commit()
        session.close()

    # Update the db with the winner
    session = Session()
    u = session.query(Artwork).get(winner)
    u.winner = True
    session.commit()
    session.close()

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
