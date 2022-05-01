"""Main class for managing query pairs: crud operations with db
 and schedule tasks
"""

from uuid import UUID


class Statistic:
    def __init__(self, session):
        self.session = session

    def add_pair(self, *, query: str, location_id: int,
                 check_every: int):
        """Check if pair of location_id and query already exists in DB and add
        a new task if needed.

        If pair is new - we create object in db and add a new task
        to the scheduler.

        If it already exists - update it`s status to "active" and "check_every",
        also update schedule
        """
        pass

    def stop_tracking_pair(self, pair_id: UUID) -> None:
        """Check existence in schedule and db, then set status to "stopped"
        as well as deleting task for pair from schedule.
        If not found - raise PairNotFound exception
        """

    def get_count_stats(self, ):
        pass

    def get_top_stats(self, ):
        pass
