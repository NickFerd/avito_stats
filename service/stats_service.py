"""Main class for managing query pairs: crud operations with db
 and schedule tasks
"""
import uuid

from database import crud
from web.api import schemas

__all__ = [
    'StatsService'
]


class StatsService:
    def __init__(self, scheduler, db_session):
        self.scheduler = scheduler
        self.session = db_session

    def add_pair(self, *, query: str, location: str,
                 check_every_minute: int):
        """Check if pair of location_id and query already exists in DB and add
        a new task if needed.
        """
        with self.session() as session:
            with session.begin():
                # Create or update pair in db
                pair_uuid = crud.upsert_pair(
                    session, query=query,
                    location=location, check_every_minute=check_every_minute
                )
                # Update schedule
                self.scheduler.add_task(
                    task_name=str(pair_uuid),
                    check_every_minute=check_every_minute
                )

        return schemas.GetPairSchema(id=pair_uuid,
                                     query=query,
                                     location=location,
                                     check_every_minute=check_every_minute)   # fixme change to dataclass

    def stop_tracking_pair(self, pair_id: uuid.UUID) -> None:
        """Check existence in schedule and db, then set appropriate status
        If not found - raise PairNotFound exception
        """
        with self.session() as session:
            with session.begin():
                crud.disable_pair(session, pair_id=pair_id)
                self.scheduler.stop_task(task_name=pair_id)

    def get_count_stats(self, ):
        pass

    def get_top_stats(self, ):
        pass
