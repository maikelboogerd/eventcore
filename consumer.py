import json
import confluent_kafka as kafka

from eventcore import Consumer


class KafkaConsumer(Consumer):
    """
    Consume from a Kafka queue.
    :param servers: list of brokers to consume from.
    :param group_id: identifier for this consumer.
    :param topics: list of topics to consume from.
    """

    def __init__(self, servers, group_id, topics):
        self.kafka_consumer = kafka.Consumer({
            'bootstrap.servers': servers,
            'group.id': group_id
        })
        self.kafka_consumer.subscribe(topics)

    def consume(self):
        while True:
            message = self.kafka_consumer.poll(1.0)
            if not message:
                continue
            if message.errors():
                continue
            message_body = json.loads(message.value())
            self.process_event(name=message_body.get('event'),
                               subject=message.key(),
                               data=message_body.get('data'))
