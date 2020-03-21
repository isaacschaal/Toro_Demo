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

# Connect to twitter
t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

def tweet_text(piece_name):
    # Return the text for the tweet
    #return "%s. Original artwork created by Toro, and Autonomous AI Artist" % piece_name
    return "%s. Testing - FFHQ" % piece_name

def tweet_img(piece_name,img_path):
    i = 0
    done = False
    id_str = "None"
    while not done and i<5:
        try:
            with open(img_path, 'rb') as photo:
                response = t.upload_media(media=photo)
            status = t.update_status(status=tweet_text(piece_name), media_ids=[response['media_id']])
            id_str = status['id_str']
            done = True
        except Exception as e:
            print(i, e)
            time.sleep(10)
            i+=1
    return done, id_str

def main(week):
    # get the paths and ids from the DB
    img_path_list = []
    ids_list = []
    name_list = []

    session = Session()
    for id,path,name in session.query(Artwork.id, Artwork.path, Artwork.name).filter_by(week = week):
        ids_list.append(id)
        img_path_list.append(path)
        name_list.append(name)
    session.close()

    # assert the length here? TODO
    failed_list = []

    for i in range(len(img_path_list)):
        # get the status and the twitter_id_str
        result, twt_id_str = tweet_img(name_list[i], img_path_list[i])

        # if it fails 5 times, deal with it TODO
        if not result:
            print ("fail")
            failed_list.append(i)
        # if it was succesfull
        else:
            # update the db with the twitter id
            session = Session()
            u = session.query(Artwork).get(ids_list[i])
            u.twitter_id_str = twt_id_str
            session.commit()
            session.close()
        # wait 10 seconds for the next tweet
        time.sleep(10)

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
