# Create the SQlite DB
# Run this once to initialize the DB

########################

# Imports
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker,scoped_session

# Create our engine
engine = db.create_engine('sqlite:///DB.sqlite')

# And use that to create a session
Session = scoped_session(sessionmaker(bind=engine))

# Build our table from the declarative_base
Base = declarative_base()

# This creates the Artwork Table,
class Artwork(Base):
    __tablename__ = 'artwork'
    # Each artwork has an ID
    id = Column(Integer, primary_key=True)
    # Each artwork is tied to a week
    week = Column(Integer)
    # Each artwork has a name
    name = Column(String)
    # The path to the img file
    path = Column(String)
    # The twitter_id of the tweet of the artwork
    twitter_id_str = Column(String)
    # The number of favorites the artwork recieved
    favorites = Column(Integer)
    # The number of RTs the artwork recieved
    RTs = Column(Integer)
    # One artwork each week is selected as the winner,
    # and winner is set to True (False otherwise)
    winner = Column( Boolean)
    # The winning image is commited to github and gets a hosting_url
    hosting_url = Column(String)
    # The winning image is minted as token and gets a tokenID
    tokenID = Column(Integer)
    # The winning image is sold at auction, this is the link
    # to the OpenSea auction
    auction_link = Column(String)

# Create all
Base.metadata.create_all(engine)
