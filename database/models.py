"""Database models
"""

import uuid

from sqlalchemy import Column, String, Boolean, Integer, UniqueConstraint
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry

from database.base import engine

_registry = registry()


@_registry.mapped
class Pair:
    """Table representing pairs of query and location_id
    """
    __tablename__ = 'pair'
    __table_args__ = (
        UniqueConstraint('query', 'location'),

    )

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True,
                default=uuid.uuid4)
    query = Column(String, nullable=False)
    location = Column(String, nullable=False)
    check_every_minute = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)


def init_db():
    """Create all tables if not exist
    """
    _registry.metadata.create_all(engine)

