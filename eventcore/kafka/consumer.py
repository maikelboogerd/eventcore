import json
import logging

from eventcore import Consumer
from eventcore.exceptions import MissingDependencyError, FatalConsumerError

log = logging.getLogger(__name__)


class KafkaConsumer(Consumer):
    """
    Consume from a Kafka queue.
    :param servers: list of brokers to consume from.
    :param group_id: identifier for this consumer.
    :param topics: list of topics to consume from.
    """

    def __init__(self, servers, group_id, topics, **kwargs):
        try:
            import confluent_kafka as kafka
            self.kafka = kafka
        except ImportError:
            raise MissingDependencyError(
                'Missing dependency run `pip install confluent-kafka`.')

        # Parse the servers to ensure it's a comma-separated string.
        if isinstance(servers, list):
            servers = ','.join(servers)
        settings = {'bootstrap.servers': servers, 'group.id': group_id}
        settings.update(kwargs)
        self.kafka_consumer = self.kafka.Consumer(settings)
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

    def is_valid_message(self, message) -> bool:
        """
        Check if the message does not have an error code.
        :param message: a `confluent_kafka.cimpl.Message` instance.
        """
        if not message:
            return False
        if message.error():
            # PARTITION_EOF error can be ignored.
            if message.error().code() == self.kafka.KafkaError._PARTITION_EOF:
                return False
            else:
                # TODO: Fix dependency.
                raise self.kafka.KafkaException(message.error())
        return True

    def parse_message(self, message) -> (str, dict):
        """
        Parse a message to retrieve the subject and message body.
        :param message: a `confluent_kafka.cimpl.Message` instance.
        """
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

        if message_body is None or not isinstance(message_body, dict):
            raise ValueError("Message body is malformed: {}".format(
                repr(message_body)))

        return subject, message_body


class BlockingKafkaConsumer(KafkaConsumer):
    """
    Consumer from Kafka topics, blocks when a message cannot be processed.
    :param servers: list of brokers to consume from.
    :param group_id: identifier for this consumer.
    :param topics: list of topics to consume from.
    """

    def __init__(self, servers, group_id, topics, **kwargs):
        kwargs['enable.auto.commit'] = False
        kwargs['auto.offset.reset'] = "smallest"  # Start from first failed.
        super().__init__(servers, group_id, topics, **kwargs)

    def poll_and_process(self):
        message = self.kafka_consumer.poll()
        if not self.is_valid_message(message):
            self.kafka_consumer.commit(message)
            return
        try:
            subject, message_body = self.parse_message(message)
        except (ValueError, AttributeError, TypeError):
            self.kafka_consumer.commit(message)
            return
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
