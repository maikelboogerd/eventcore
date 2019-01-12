import json

from eventcore import Producer
from eventcore.exceptions import MissingDependencyError
from eventcore.kafka.header import Header


class KafkaProducer(Producer):
    """
    Produce to a Kafka queue.
    :param servers: list of brokers to consume from.
    :param servers: The host and port of where Kafka runs.
    :param source: The source of the application which is producing the
    messages.
    """

    source = ''

    def __init__(self, servers, source=None):
        try:
            import confluent_kafka as kafka
        except ImportError:
            raise MissingDependencyError(
                'Missing dependency run `pip install confluent-kafka`.')

        self.source = source

        # Parse the servers to ensure it's a comma-separated string.
        if isinstance(servers, list):
            servers = ','.join(servers)
        self.kafka_producer = kafka.Producer({
            'bootstrap.servers': servers
        })

    def get_headers(self, event):
        """
        Creates an header which is added to Kafka
        :param event: the name of the event e.g user.created
        :return: a json serialized representation of the header
        """
        header = Header(source=self.source, event=event)
        return header.__dict__

    def produce(self, topic, event, subject, data):
        message_body = json.dumps({
            'event': event,
            'data': data
        })
        self.kafka_producer.produce(topic=topic,
                                    key=subject,
                                    value=message_body,
                                    headers=self.get_headers(event))
