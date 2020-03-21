import argparse
import subprocess
from create_db import Artwork, Session
from datetime import date



# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--d", type=str, help="The date")

def main(week):
    # 1: Choose Winner
    commands = ['python3', 'tw_choose_winner_friday.py','--week',str(week)]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    if process.returncode == 0:

        # 2: Mint token and add metadata
        commands = ['python3', 'mint_friday.py','--week',str(week)]
        process = subprocess.run(commands,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

        if process.returncode == 0:
            # 3: Create auction
            # Get the tokenid and favorite count
            session = Session()
            tokenID, favorites  = session.query(Artwork.tokenID, Artwork.favorites).filter_by(week = week, winner = True).first()
            session.close()

            # run the node auction script
            commands = ['node', 'AA_smart_contract_rinkeby/scripts/sell.js',
                        '-f',str(favorites),
                        '-i',str(tokenID)]
            process = subprocess.run(commands,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)

            if process.returncode == 0:
                # 4: Tweet auction
                stdout = process.stdout

                # get the auction link
                auction_link = stdout.split("order!",1)[1].strip()

                # save it to the DB
                session = Session()
                u  = session.query(Artwork).filter_by(week = week, winner = True).first()
                u.auction_link =  auction_link
                session.commit()
                session.close()

                commands = ['python3', 'tweet_auction_friday.py','--week',str(week)]
                process = subprocess.run(commands,
                                        stdout=subprocess.PIPE,
                                        universal_newlines=True)
                #process



    else:
        print (process)



if __name__ == '__main__':
    args = parser.parse_args()
    d = args.d
    # base date
    d0 = date(2020, 3, 3)
    # current date
    d1 = d.split("-")
    d1 = date(int(d1[0]),int(d1[1]),int(d1[2]))
    delta = d1 - d0
    # for daily minting, the main_friday will be -1
    main(delta.days -1)
