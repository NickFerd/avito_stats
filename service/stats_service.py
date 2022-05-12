"""Main class for managing query pairs: crud operations with db
 and schedule tasks
"""
import uuid

from sqlalchemy import select

from database.models import Pair
from web.api import schemas
from service import exceptions as exc


class StatsService:
    def __init__(self, scheduler, db_session):
        self.scheduler = scheduler
        self.session = db_session

    def add_pair(self, *, query: str, location: str,
                 check_every_minute: int):
        """Check if pair of location_id and query already exists in DB and add
        a new task if needed.
        """
        get_pair_stmt = select(Pair).where(Pair.query == query).where(
            Pair.location == location)
        with self.session() as session:
            with session.begin():
                # Create or update pair in db
                existing_pair = session.execute(get_pair_stmt).one_or_none()
                if existing_pair:
                    # Pair exists
                    pair = existing_pair[0]
                    pair.check_every_minute = check_every_minute
                    pair.status = True
                    pair_uuid = pair.id
                else:
                    # Create new pair
                    pair_uuid = uuid.uuid4()

                    pair = Pair(id=str(pair_uuid),
                                query=query,
                                location=location,
                                check_every_minute=check_every_minute,
                                status=True)
                    session.add(pair)

                # Update schedule
                self.scheduler.add_task(
                    task_name=str(pair_uuid),
                    check_every_minute=check_every_minute
                )

        return schemas.GetPairSchema(id=pair_uuid,
                                     query=query,
                                     location=location,
                                     check_every_minute=check_every_minute)

    def stop_tracking_pair(self, pair_id: str) -> None:
        """Check existence in schedule and db, then set appropriate status
        If not found - raise PairNotFound exception
        """
        get_pair_stmt = select(Pair).where(Pair.id == pair_id)
        with self.session() as session:
            with session.begin():
                existing_pair = session.execute(get_pair_stmt).one_or_none()
                if not existing_pair:
                    raise exc.PairNotFound('Pair not found')

                pair = existing_pair[0]
                pair.status = False
                entry = self.scheduler.stop_task(task_name=pair_id)

    def get_count_stats(self, ):
        pass

    def get_top_stats(self, ):
        pass
