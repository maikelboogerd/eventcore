import json
import uuid

from eventcore import Producer
from eventcore.exceptions import MissingDependencyError


class SQSProducer(Producer):
    """
    Produce to a SQS queue.
    :param region_name:
    :param access_key_id:
    :param secret_access_key:
    :param queue_url:
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

    def produce(self, topic, event, subject, data):
        """
        """
        message_body = {
            'event': event,
            'subject': subject,
            'data': data
        }
        self.queue.send_message(MessageBody=json.dumps(message_body),
                                MessageGroupId=topic,
                                MessageDeduplicationId=str(uuid.uuid4()))
