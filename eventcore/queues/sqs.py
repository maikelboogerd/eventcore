import json
import uuid
import boto3

from eventcore import Queue, Message


class SQSQueue(Queue):
    def __init__(self,
                 region_name,
                 access_key_id,
                 secret_access_key,
                 url):
        sqs = boto3.resource('sqs',
                             region_name=region_name,
                             aws_access_key_id=access_key_id,
                             aws_secret_access_key=secret_access_key)
        self._queue = sqs.Queue(url)

    def read(self, topic=None):
        for resource in self._queue.receive_messages(MaxNumberOfMessages=10):
            message_body = json.loads(resource.body)
            message = self.prepare(topic=None,
                                   event=message_body.get('event'),
                                   subject=message_body.get('subject'),
                                   data=message_body.get('data'))
            message.message_id = resource.message_id
            message.receipt_handle = resource.receipt_handle
            yield message

    def enqueue(self, message):
        message_body = {
            'event': message.event,
            'subject': message.subject,
            'data': message.data
        }
        self._queue.send_message(MessageBody=json.dumps(message_body),
                                 MessageGroupId=message.topic,
                                 MessageDeduplicationId=str(uuid.uuid4()))

    def dequeue(self, message):
        self._queue.delete_messages(Entries=[{
            'Id': message.message_id,
            'ReceiptHandle': message.receipt_handle
        }])

    def prepare(self, topic, event, subject, data):
        return SQSMessage(topic, event, subject, data)


class SQSMessage(Message):
    message_id = None
    receipt_handle = None
