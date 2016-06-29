from sqlalchemy import create_engine, Date, String, Column, Integer

import os

engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Deadline(Base):
    __tablename__ = 'deadlines'

    id = Column(Integer,primary_key=True)
    date = Column(Date)
    item = Column(String)

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
