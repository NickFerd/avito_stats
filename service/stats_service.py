"""Main class for managing query pairs: crud operations with db
 and schedule tasks
"""
import uuid
from dataclasses import asdict
from datetime import datetime

from database import crud
from service.utils import PairItem, CountStat, AdsStat

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

        return PairItem(id=pair_uuid,
                        query=query,
                        location=location,
                        check_every_minute=check_every_minute)

    def stop_tracking_pair(self, pair_id: uuid.UUID) -> None:
        """Check existence in schedule and db, then set appropriate status
        If not found - raise PairNotFound exception
        """
        with self.session() as session:
            with session.begin():
                crud.disable_pair(session, pair_id=pair_id)
                self.scheduler.stop_task(task_name=pair_id)

    def get_count_stats(self, pair_id: uuid.UUID,
                        datetime_from: datetime, datetime_to: datetime):
        """Get count stat for provided pair_id and period"""
        with self.session() as session:
            with session.begin():
                full_stats = crud.get_stats_for_pair_and_period(
                    session,
                    pair_id=pair_id,
                    period_from=datetime_from,
                    period_to=datetime_to
                )
                stats = []
                for stat in full_stats:
                    stats.append(CountStat(moment=stat.moment,
                                           count=stat.count))

        return stats

    def get_top_stats(self, pair_id: uuid.UUID,
                      datetime_from: datetime, datetime_to: datetime):
        """Get top ads for provided pair and period"""
        with self.session() as session:
            with session.begin():
                full_stats = crud.get_stats_for_pair_and_period(
                    session,
                    pair_id=pair_id,
                    period_from=datetime_from,
                    period_to=datetime_to
                )
                stats = []
                for stat in full_stats:
                    stats.append(AdsStat(moment=stat.moment,
                                         ads=stat.ads))
        return stats
