from .event import Event # noqa
from .producer import Producer # noqa
from .consumer import Consumer # noqa
from .decorators import event_subscriber, dispatch_event # noqa


class DummyQueue(object):
    _queue = []

    @classmethod
    def add(cls, message):
        cls._queue.append(message)

    @classmethod
    def read(cls):
        for message in cls._queue:
            yield message

    @classmethod
    def remove(cls, message):
        cls._queue.remove(message)


class DummyMessage(object):
    def __init__(self, topic, event, subject, data):
        self.topic = topic
        self.event = event
        self.subject = subject
        self.data = data


class DummyProducer(Producer):
    def produce(self, topic, event, subject, data):
        message = DummyMessage(topic, event, subject, data)
        DummyQueue.add(message)


class DummyConsumer(Consumer):
    def consume(self):
        for message in DummyQueue.read():
            self.process_event(message.event, message.subject, message.data)
            DummyQueue.remove(message)


def includeme(config):
    producer = DummyProducer()
    producer.set_default()
    consumer = DummyConsumer()
    consumer.consume()
