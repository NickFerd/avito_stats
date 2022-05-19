"""Util functions for performing CRUD operations with SQLAlchemy
"""
import uuid
from typing import Union

from sqlalchemy import select

from database.base import LocalSession
from database.models import Pair
from service import exceptions as exc

__all__ = [
    'get_pair_by_id',
    'upsert_pair',
    'disable_pair'
]


def get_pair_by_id(session: LocalSession,
                   pair_id: Union[str, uuid.UUID]) -> Pair:
    """Get pair item by id or raise PairNotFound error
    """
    get_pair_stmt = select(Pair).where(Pair.id == pair_id)

    pair = session.execute(get_pair_stmt).scalar()
    if not pair:
        raise exc.PairNotFound(f'Pair with id={pair_id} not found')

    return pair


def upsert_pair(session: LocalSession, query: str, location: str,
                check_every_minute: int) -> uuid.UUID:
    """Update or insert a new pair item
    """
    get_pair_stmt = select(Pair).where(Pair.query == query).where(
        Pair.location == location)

    pair = session.execute(get_pair_stmt).scalar()
    if pair:
        # Pair exists
        pair.check_every_minute = check_every_minute
        pair.status = True
        pair_uuid = pair.id
    else:
        # Create new pair
        pair_uuid = uuid.uuid4()

        pair = Pair(id=pair_uuid,
                    query=query,
                    location=location,
                    check_every_minute=check_every_minute,
                    status=True)
        session.add(pair)

    return pair_uuid


def disable_pair(session: LocalSession, pair_id: uuid.UUID):
    """Set boolean status field to False
    """
    pair = get_pair_by_id(session, pair_id)
    pair.status = False
