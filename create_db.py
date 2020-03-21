import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker,scoped_session


engine = db.create_engine('sqlite:///DB.sqlite')

Session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()

class Artwork(Base):
    __tablename__ = 'artwork'
    id = Column(Integer, primary_key=True)
    week = Column(Integer)
    name = Column(String)
    path = Column(String)
    twitter_id_str = Column(String)
    favorites = Column(Integer)
    RTs = Column(Integer)
    winner = Column( Boolean)
    hosting_url = Column(String)
    tokenID = Column(Integer)
    auction_link = Column(String)

Base.metadata.create_all(engine)
