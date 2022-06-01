"""Database models
"""

import uuid

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    TIMESTAMP,
    UniqueConstraint,
    ForeignKey
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import registry, relationship

from database.base import engine

_registry = registry()

__all__ = [
    'Pair',
    'Stat',
    'init_db'
]


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

    stats = relationship("Stat")


@_registry.mapped
class Stat:
    """Model of table containing results of tasks execution
    """
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True)
    pair_id = Column(postgresql.UUID(as_uuid=True), ForeignKey('pair.id'))
    moment = Column(TIMESTAMP(timezone=True))
    count = Column(Integer, nullable=False)
    ads = Column(postgresql.JSONB)

    def __repr__(self) -> str:
        return f'<Stat> pair_id={self.pair_id}, moment={self.moment}'


def init_db():
    """Create all tables if not exist
    """
    _registry.metadata.create_all(engine)

