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
    :param server_auto_commit: when enabled, the consumer will issue no commits
    :param commit_after_processing: commits to the log after successfully 
    processing a message. 
    """

    def __init__(self,
                 servers,
                 group_id,
                 topics,
                 server_auto_commit=False,
                 commit_after_processing=False):
        # Parse the servers to ensure it's a comma-separated string.
        if isinstance(servers, list):
            servers = ','.join(servers)
        self.server_auto_commit = server_auto_commit
        self.commit_after_process = commit_after_processing
        self.kafka_consumer = kafka.Consumer({
            'bootstrap.servers': servers,
            'group.id': group_id
        })
        # Parse the topics to ensure it's a list.
        if isinstance(topics, str):
            topics = topics.split(',')

        self.kafka_consumer.subscribe(topics)

    def consume(self):
        while True:
            self.poll_and_process()

    def poll_and_process(self):
        message = self.kafka_consumer.poll(1.0)
        if not message:
            return
        if message.error():
            # PARTITION_EOF error can be ignored.
            if message.error().code() == kafka.KafkaError._PARTITION_EOF:
                return
            else:
                raise kafka.KafkaException(message.error())
        if not self.server_auto_commit and not self.commit_after_process:
            self.kafka_consumer.commit(message)
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

        self.process_event(
            name=message_body.get('event'),
            subject=subject,
            data=message_body.get('data'))
        if self.commit_after_process:
            self.kafka_consumer.commit(message)
