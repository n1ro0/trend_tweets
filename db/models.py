from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, create_engine
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()


class Tweet(Base):
    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True)
    created_at = Column(String)
    username = Column(String)
    text = Column(Text)


class Hashtag(Base):
    __tablename__ = "hashtags"
    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey('products.id'))
    text = Column(String)


ENGINE = create_engine('postgresql://test_user:qwerty12@localhost/test_db')
Base.metadata.bind = ENGINE
Base.metadata.create_all()
SESSIONMAKER = sessionmaker(bind=ENGINE)
