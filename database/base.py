"""Database related objects and functions"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_uri = os.environ['DB_URI']   # todo maybe make pydantic config
engine = create_engine(db_uri, future=True)
LocalSession = sessionmaker(engine, future=True)

