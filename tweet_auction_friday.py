from twython import Twython
import os
import time
import argparse
from create_db import Artwork, Session


parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

# Get env
TWITTER_APP_KEY = os.getenv('TWITTER_APP_KEY')
TWITTER_APP_KEY_SECRET = os.getenv('TWITTER_APP_KEY_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

def auction_text(piece_name, auction_link):
  return "%s is now for sale on OpenSea! The auction will last for 1 week. %s" % (piece_name,auction_link)

def auction_tweet(piece_name,auction_link):
    done = False
    i = 0
    while not done and i<5:
        try:
          t.update_status(status=auction_text(piece_name, auction_link))
          done = True

        except Exception as e:
          print(i, e)
          time.sleep(10)
          i+=1
    return done

def main(week):
    session = Session()
    piece_name, auction_link = session.query(Artwork.name,
                                            Artwork.auction_link).\
                                            filter_by(week = week, winner = True).first()

    session.close()

    result = auction_tweet(piece_name,auction_link)



if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
