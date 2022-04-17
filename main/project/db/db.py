from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///trends.sqlite')
Session = sessionmaker(bind=engine)
session: sessionmaker = Session()

Base = declarative_base()