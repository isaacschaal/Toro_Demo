# This script is used to generate new images, add them to the DB,
# and tweet the images. It is a wrapper script that calls other scripts
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

########################

# Imports
import argparse
import subprocess
from datetime import date

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--d", type=str, help="The date")

def main(week):
    # 1: Generate new images
    commands = ['python3', 'scripts/generate_new_imgs.py','--week',str(week)]
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)

    if process.returncode == 0:
        # 2: Add new images to DB
        commands = ['python3', 'scripts/add_new_imgs_to_DB.py','--week',str(week)]
        process = subprocess.run(commands,
                                stdout=subprocess.PIPE,
                                universal_newlines=True)

        if process.returncode == 0:
            # 3: Tweet new images
            commands = ['python3', 'scripts/tweet_new_imgs.py','--week',str(week)]
            process = subprocess.run(commands,
                                    stdout=subprocess.PIPE,
                                    universal_newlines=True)
        else:
            # If adding to the DB failed
            print ("fail 2")
            print (process)
    else:
        # If the image generation failed
        print ("fail 1")
        print (process)

    # 4: Send ETH
    commands = ['node', 'Toro_smart_contract/scripts/send_eth.js']
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    # Note, for demo purposes, this just sends ETH to an address I control,
    # but a live version would send ETH to the address provided by the
    # webhosting service


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
    # Pass this as the 'week' variable
    delta = d1 - d0
    main(delta.days)
