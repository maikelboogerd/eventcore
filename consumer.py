import json
import logging

import confluent_kafka as kafka

from eventcore import Consumer

log = logging.getLogger(__name__)


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
            if message.error():
                # PARTITION_EOF error can be ignored.
                if message.error().code() == kafka.KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise kafka.KafkaException(message.error())

            try:
                message_body = json.loads(message.value())
            except TypeError:
                message_body = json.loads(message.value().decode('utf-8'))
            except:
                log.error('@KafkaConsumer.consume Exception:',
                          exc_info=True)
            self.process_event(name=message_body.get('event'),
                               subject=message.key(),
                               data=message_body.get('data'))
