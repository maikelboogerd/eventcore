import logging

from eventcore import Consumer
from eventcore.exceptions import MissingDependencyError

LOGGER = logging.getLogger(__name__)


class DatabaseConsumer(Consumer):
    """
    Consume from a `PostgreSQL` database.
    """

    def __init__(self):
        try:
            import psycopg2
        except ImportError:
            raise MissingDependencyError(
                'Missing dependency run `pip install psycopg2`.')

        # TODO: Somehow get the connection.
        self.connection = None

    def consume(self):
        """
        """
        while True:
            # TODO: Get 'new' events from the database.
            # TODO: Maybe set a 1s interval?
            pass
