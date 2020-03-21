#!/usr/bin/env python
import argparse
import subprocess
from datetime import date


# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--d", type=str, help="The date")

def main(week):
    # 1: Generate new images
    commands = ['python3', 'generate_images_monday.py','--week',str(week)]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    if process.returncode == 0:
        # 2: Add new images to DB
        commands = ['python3', 'add_new_imgs_to_DB_monday.py','--week',str(week)]
        process = subprocess.run(commands,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

        if process.returncode == 0:
            # 3: Tweet new images
            commands = ['python3', 'tweet_new_imgs_monday.py','--week',str(week)]
            process = subprocess.run(commands,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
            #process
        else:
            print ("fail 2")
            print (process)
    else:
        print ("fail 1")
        print (process)

    # 4: Take inventory of ETH and make appropriate sales if needed
    # possibly split this into two functions and do the logic in python ?
    commands = ['node', 'AA_smart_contract_rinkeby/scripts/send_eth.js']
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)


if __name__ == '__main__':
    args = parser.parse_args()
    d = args.d
    # base date
    d0 = date(2020, 3, 3)
    # current date
    print(d)
    #d = d[1:-1]
    d1 = d.split("-")
    d1 = date(int(d1[0]),int(d1[1]),int(d1[2]))
    delta = d1 - d0
    main(delta.days)
