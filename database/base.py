"""Database related objects and functions"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

engine = create_engine(settings.db_uri, future=True)
LocalSession = sessionmaker(engine, future=True)

__all__ = [
    LocalSession,
    engine
]
