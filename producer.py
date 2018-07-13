import confluent_kafka as kafka

from eventcore import Producer


class KafkaProducer(Producer):
    """
    Produce to a Kafka queue.
    :param servers: list of brokers to consume from.
    """

    def __init__(self, server):
        self.kafka_producer = kafka.Producer({
            'bootstrap.servers': server
        })

    def produce(self, topic, event, subject, data):
        pass
