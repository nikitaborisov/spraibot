from sqlalchemy import create_engine, Date, String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

engine = create_engine(os.environ.get('DATABASE_URL'), echo=True)


Base = declarative_base()


class Deadline(Base):
    __tablename__ = 'deadlines'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    item = Column(String)


Session = sessionmaker(bind=engine)
