import json
import confluent_kafka as kafka

from eventcore import Producer


class KafkaProducer(Producer):
    """
    Produce to a Kafka queue.
    :param servers: list of brokers to consume from.
    """

    def __init__(self, servers):
        self.kafka_producer = kafka.Producer({
            'bootstrap.servers': servers
        })

    def produce(self, topic, event, subject, data):
        message_body = {
            'event': event,
            'data': data
        }
        self.kafka_producer.produce(topic=topic,
                                    key=subject,
                                    value=json.dumps(message_body))
