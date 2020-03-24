# This function adds the newly created images to the DB
# It is called by the main_generate.py function

# It recieves the week as input, and uses that to select the
# appropriate img_folder_path (along with saving the week to the DB)

########################

# Imports
import argparse
import os
from create_db import Artwork, Session

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

def main(week):
    # Get the img_folder_path where the new images are
    img_folder_path = "img_folders/week_"+str(week)+"/"
    img_list = os.listdir(img_folder_path)
    # Get the individual image file names
    img_list = [img for img in img_list if img[-4:]==".png"]

    # Iterate through the images
    for i in range(len(img_list)):
        # Open a DB session
        session = Session()
        # Add the new artwork
        session.add(
                    Artwork(week = week,
                        # The image name is based on the week
                        # and the order of generated images that week
                        name = "Unititled (" + str(week)+"-"+str(i+1)+")",
                        path = img_folder_path +img_list[i],
                        # Have blank values for all other dimensions.
                        twitter_id_str = "_",
                        favorites = "_",
                        RTs = "_",
                        winner= False,
                        hosting_url = "_",
                        tokenID = "_",
                        auction_link = "_"))
        # Commit the new entry to the DB
        session.commit()
        # Close the session
        session.close()

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
