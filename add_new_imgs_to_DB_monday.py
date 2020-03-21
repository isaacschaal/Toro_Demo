import argparse
import os
from create_db import Artwork, Session

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

def main(week):
    img_folder_path = "img_folders/week_"+str(week)+"/"
    img_list = os.listdir(img_folder_path)
    img_list = [img for img in img_list if img[-4:]==".png"]

    for i in range(len(img_list)):
        session = Session()
        session.add(
                    Artwork(week = week,
                        name = "Unititled (" + str(week)+"-"+str(i+1)+")",
                        path = img_folder_path +img_list[i],
                        twitter_id_str = "_",
                        favorites = "_",
                        RTs = "_",
                        winner= False,
                        hosting_url = "_",
                        tokenID = "_",
                        auction_link = "_"))
        session.commit()
        session.close()

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
