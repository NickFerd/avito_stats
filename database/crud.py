"""Util functions for performing CRUD operations with SQLAlchemy
"""
import uuid

from sqlalchemy import select

from database.base import LocalSession
from database.models import Pair
from service import exceptions as exc


def upsert_pair(session: LocalSession, query: str, location: str,
                check_every_minute: int) -> uuid.UUID:
    """Update or insert a new pair item
    """
    get_pair_stmt = select(Pair).where(Pair.query == query).where(
        Pair.location == location)

    existing_pair = session.execute(get_pair_stmt).one_or_none()
    if existing_pair:
        # Pair exists
        pair = existing_pair[0]  # Unpacking Row object
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
    If no pair exists - raise PairNotFound"""
    get_pair_stmt = select(Pair).where(Pair.id == pair_id)

    existing_pair = session.execute(get_pair_stmt).one_or_none()
    if not existing_pair:
        raise exc.PairNotFound('Pair not found')

    pair = existing_pair[0]  # Unpacking Row object
    pair.status = False
