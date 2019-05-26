import logging
import json

from eventcore import Consumer
from eventcore.exceptions import MissingDependencyError

LOGGER = logging.getLogger(__name__)


class SQSConsumer(Consumer):
    """
    Consume from a SQS queue.
    :param region_name: the AWS region this queue is in.
    :param access_key_id: your AWS Access Key ID.
    :param secret_access_key: your AWS Secret Access Key.
    :param queue_url: url endpoint for the queue.
    """

    def __init__(self,
                 region_name,
                 access_key_id,
                 secret_access_key,
                 queue_url):
        try:
            import boto3
        except ImportError:
            raise MissingDependencyError(
                'Missing dependency run `pip install boto3`.')

        sqs = boto3.resource('sqs',
                             region_name=region_name,
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key)
        self.queue = sqs.Queue(queue_url)

    def consume(self):
        """
        Retrieve message and trigger `process_event` on every message returned.
        """
        while True:
            self.sleep()
            for message in self.queue.receive_messages(MaxNumberOfMessages=10):
                try:
                    message_body = json.loads(message.body)
                    self.process_event(name=message_body.get('event'),
                                       subject=message_body.get('subject'),
                                       data=message_body.get('data'))
                    self.queue.delete_messages(Entries=[{
                        'Id': message.message_id,
                        'ReceiptHandle': message.receipt_handle
                    }])
                except:
                    LOGGER.error('@SQSConsumer.consume Exception:',
                                 exc_info=True)
                    continue
