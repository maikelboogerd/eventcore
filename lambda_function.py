from eventcore import Consumer, Event, event_subscriber
from eventcore.queues import DummyQueue


class UserCreated(Event):
    name = 'UserCreated'
    topic = 'User'


@event_subscriber(UserCreated)
def send_activation(event):
    print('@send_activation')


def lambda_handler(event, context):
    queue = DummyQueue()
    consumer = Consumer(queue)
    consumer.consume()
