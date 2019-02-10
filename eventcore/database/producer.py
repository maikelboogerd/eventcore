from eventcore import Producer
from eventcore.exceptions import MissingDependencyError


class DatabaseProducer(Producer):
    """
    Produce to a `PostgreSQL` database.
    """

    def __init__(self):
        try:
            import psycopg2
        except ImportError:
            raise MissingDependencyError(
                'Missing dependency run `pip install psycopg2`.')

        # TODO: Somehow get the connection.
        self.connection = None

    def produce(self, topic, event, subject, data):
        """
        """
        # TODO: Save event in the database.
        pass
