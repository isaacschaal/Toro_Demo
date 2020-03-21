import os
import time
import argparse
from twython import Twython
from create_db import Artwork, Session


parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

TWITTER_APP_KEY = os.getenv('TWITTER_APP_KEY')
TWITTER_APP_KEY_SECRET = os.getenv('TWITTER_APP_KEY_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
SCREEN_NAME=os.getenv('SCREEN_NAME')


t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)


def keyswithmaxval(d):
    v=list(d.values())
    max_v = max(v)

    k=list(d.keys())
    max_keys = []
    for i in range(len (k)):
        if d[k[i]] == max_v:
            max_keys.append(k[i])
    return max_keys




def main(week):
    # Get id str and ids list from DB
    session = Session()
    ids_list = [id[0] for id in session.query(Artwork.id).filter_by(week = week ).all()]
    ids_list.sort()

    twt_id_str_dic = {}
    for id in ids_list:
        twt_id_str_dic[id] = session.query(Artwork.twitter_id_str).filter_by(id = id).first()[0]


    favorites_dic = {}
    RTs_dic = {}

    timeline = t.get_user_timeline(screen_name = SCREEN_NAME )

    success = [False for i in range(5)]
    for i,id in enumerate(ids_list):
        twt_id_str = twt_id_str_dic[id]
        for tweet in timeline:
            if tweet['id_str'] == twt_id_str:
                favorites_dic[id] = tweet['favorite_count']
                RTs_dic[id] = tweet['retweet_count']
                ## ADD Fav and RT to db (if needed)
                success[i] = True
                break
    # CHECK IF I GOT THE correct 5 TWEETS

    # get the key with most likes
    max_favorites_keys = keyswithmaxval(favorites_dic)

    # if there is a tie, get RTs
    if len(max_favorites_keys) >1:
        #get RTs
        RTs_of_max_favorites = { key: RTs_dic[key] for key in max_favorites_keys }
        #get the max
        max_RTs_keys = keyswithmaxval(RTs_of_max_favorites)
        # if theres another tie
        if len(max_RTs_keys) >1:
            #choose the biggest key, as it was tweeted last (TIE BREAKER)
            winner = max(max_RTs_keys)
        # winner tied likes but most RTs
        else:
            winner = max_RTs_keys[0]
    # winner had most likes
    else:
        winner = max_favorites_keys[0]

    # update the db with the favs and RTs
    for id in ids_list:
        session = Session()
        u = session.query(Artwork).get(id)
        u.favorites = favorites_dic[id]
        u.RTs = RTs_dic[id]
        session.commit()
        session.close()

    # update the db with the winner
    session = Session()
    u = session.query(Artwork).get(winner)
    u.winner = True
    session.commit()
    session.close()

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
