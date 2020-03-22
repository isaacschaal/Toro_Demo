# This script is used to choose the winning image, mint the token and upload
# the metadata, and create and tweet about an auction.
# It is a wrapper script that calls other scripts
# (using subprocess) to complete each task

# This script is called by main_timer.py

# This script recieves the current date and uses that to
# calculate the correct week

# Note, the variable 'week' is used to keep track
# of succesive iterations of generating and minting images.
# As the code currently is written for this demo, these iterations
# take place once a day, so it is easier for the graders to interact
# with it. The variable 'week' is kept, as it will be the length of time
# used in the live version.

# Imports
import argparse
import subprocess
from create_db import Artwork, Session
from datetime import date

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--d", type=str, help="The date")

def main(week):
    # 1: Choose Winner
    commands = ['python3', 'scripts/choose_winner.py','--week',str(week)]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    if process.returncode == 0:

        # 2: Mint token and add metadata
        commands = ['python3', 'scripts/mint.py','--week',str(week)]
        process = subprocess.run(commands,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

        if process.returncode == 0:
            # 3: Create auction
            # Get the tokenid and favorite count
            session = Session()
            tokenID, favorites  = session.query(Artwork.tokenID, Artwork.favorites).filter_by(week = week, winner = True).first()
            session.close()

            # Run the node auction script
            commands = ['node', 'Toro_smart_contract/scripts/sell.js',
                        '-f',str(favorites),
                        '-i',str(tokenID)]
            process = subprocess.run(commands,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)

            if process.returncode == 0:
                # 4: Tweet auction
                stdout = process.stdout

                # Get the auction link
                auction_link = stdout.split("order!",1)[1].strip()

                # Save it to the DB
                session = Session()
                u = session.query(Artwork).filter_by(week = week, winner = True).first()
                u.auction_link =  auction_link
                session.commit()
                session.close()

                # Send the tweet
                commands = ['python3', 'scripts/tweet_auction.py','--week',str(week)]
                process = subprocess.run(commands,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)

if __name__ == '__main__':
    args = parser.parse_args()
    d = args.d
    # For the demo version, this script
    # is called each day and increments the 'week' variable
    # once each day

    # Base date
    d0 = date(2020, 3, 20)

    # Current date
    d1 = d.split("-")
    d1 = date(int(d1[0]),int(d1[1]),int(d1[2]))

    # Find the difference between the two dates
    delta = d1 - d0

    # In the demo, the minting happens the day after the generating,
    # but is tied to the same 'week' variable, so we use delta -1
    main(delta.days -1)
