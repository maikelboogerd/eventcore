import json
import logging
from typing import Tuple

import confluent_kafka as kafka
from confluent_kafka.cimpl import Message
from eventcore import Consumer
from eventcore.exceptions import FatalConsumerError

log = logging.getLogger(__name__)


class KafkaConsumer(Consumer):
    """
    Consume from a Kafka queue.
    :param servers: list of brokers to consume from.
    :param group_id: identifier for this consumer.
    :param topics: list of topics to consume from.
    """

    def __init__(self, servers, group_id, topics, **kwargs):
        # Parse the servers to ensure it's a comma-separated string.
        if isinstance(servers, list):
            servers = ','.join(servers)
        self.kafka_consumer = kafka.Consumer({
            'bootstrap.servers': servers,
            'group.id': group_id,
            **kwargs
        })
        # Parse the topics to ensure it's a list.
        if isinstance(topics, str):
            topics = topics.split(',')

        self.kafka_consumer.subscribe(topics)

    def consume(self):
        while True:
            self.poll_and_process()

    def poll_and_process(self):
        message = self.kafka_consumer.poll()
        if not self.is_valid_message(message):
            return
        subject, message_body = self.parse_message(message)
        self.process_event(
            name=message_body.get('event'),
            subject=subject,
            data=message_body.get('data'))

    @staticmethod
    def is_valid_message(message: Message):
        if not message:
            return False
        if message.error():
            # PARTITION_EOF error can be ignored.
            if message.error().code() == kafka.KafkaError._PARTITION_EOF:
                return False
            else:
                raise kafka.KafkaException(message.error())
        return True

    @staticmethod
    def parse_message(message: Message) -> Tuple[str, dict]:
        subject, message_body = None, None
        try:
            message_body = json.loads(message.value())
        except TypeError:
            message_body = json.loads(message.value().decode('utf-8'))
        except:
            log.error('@KafkaConsumer.consume Exception:', exc_info=True)
        try:
            subject = message.key().decode('utf-8')
        except AttributeError:
            subject = message.key()

        return subject, message_body


class BlockingKafkaConsumer(KafkaConsumer):
    """Consumer for Kafka topics, blocks when a message cannot be processed."""

    def __init__(self, servers, group_id, topics, **kwargs):
        kwargs['enable.auto.commit'] = False
        kwargs['auto.offset.reset'] = "smallest"  # Start from first failed.
        super().__init__(servers, group_id, topics, **kwargs)

    def poll_and_process(self):
        message = self.kafka_consumer.poll()
        if not self.is_valid_message(message):
            return
        subject, message_body = self.parse_message(message)
        try:
            self.process_event(
                name=message_body.get('event'),
                subject=subject,
                data=message_body.get('data'))
            self.kafka_consumer.commit(message)
        except BaseException:
            raise FatalConsumerError(
                "Message with body {} could not be processed and blocks "
                "the consumer. Manual action required.".format(message_body))
