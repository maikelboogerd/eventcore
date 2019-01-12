import json
import confluent_kafka as kafka
from eventcore_kafka.header import Header

from eventcore import Producer


class KafkaProducer(Producer):
    """
    Produce to a Kafka queue.
    :param servers: list of brokers to consume from.
    """

    source = ''

    def __init__(self, servers, source=None):
        """
        Initialize the producer for Kafka
        :param servers: The host and port of where Kafka runs.
        :param source: The source of the application which is producing the
        messages.
        """

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
