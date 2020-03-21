import time
import argparse
from PIL import Image
import sh
import subprocess
from create_db import Artwork, Session
import json

# Parse Args
parser = argparse.ArgumentParser()
parser.add_argument("--week", type=str, help="The number of the week")

def main(week):
    # get the winner
    session = Session()
    db_id, name, path  = session.query(Artwork.id, Artwork.name, Artwork.path).filter_by(week = week, winner = True).first()
    session.close()

    # save the image to the repo
    with Image.open(path) as img:
        img = img.save("metadata_hosting/image_hosting/"+name+".jpg")

    # encode the name as url
    name_urld = name.replace(" ", "%20")

    # make the image link
    img_link = "https://raw.githubusercontent.com/isaacschaal/metadata_hosting/master/image_hosting/"+name_urld + ".jpg"

    # make the metadata_dic
    metadata = {
      #"description": "One of a kind original artwork made by Toro, an Autonomous AI artist.",
      "description": "Test Artwork.",
      "image": img_link,
      "name": str(name),
      "attributes": [
        {
          "trait_type": "size",
          "value": "1024x1024"
        },
        {
          "trait_type": "format",
          "value": ".png"
        }
      ]
    }

    # mint the token
    commands = ['node', 'AA_smart_contract_rinkeby/scripts/mint.js']
    process = subprocess.run(commands,
                            stdout=subprocess.PIPE,
                            universal_newlines=True)
    # CHECK THAT IT WAS SUCCESFUL!
    # IF IT WAS

    # Get the token_id from stdout
    stdout = process.stdout
    token_id = int(stdout.split("Token ID:",1)[1].strip())

    # add token_id to DB
    session = Session()
    u = session.query(Artwork).get(db_id)
    u.tokenID = token_id
    session.commit()
    session.close()

    # save the metadata to the repo
    f = open("./metadata_hosting/"+str(token_id),"w")
    f.write( json.dumps(metadata) )
    f.close()

    # commit the changes and push them
    git = sh.git.bake(_cwd='./metadata_hosting/')
    print(git.add('-A'))
    print(git.commit(m='added new images and metadata'))
    print(git.push())

if __name__ == '__main__':
    args = parser.parse_args()
    week = args.week
    main(week)
