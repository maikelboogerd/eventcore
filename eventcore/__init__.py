from .event import Event # noqa
from .producer import Producer # noqa
from .consumer import Consumer # noqa
from .decorators import event_subscriber, dispatch_event # noqa


class DummyQueue(object):
    _messages = []

    @classmethod
    def add(cls, message):
        cls._messages.append(message)

    @classmethod
    def read(cls):
        for message in cls._messages:
            yield message

    @classmethod
    def remove(cls, message):
        cls._messages.remove(message)


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
        while True:
            for message in DummyQueue.read():
                self.process_event(name=message.event,
                                   subject=message.subject,
                                   data=message.data)
                DummyQueue.remove(message)


def includeme(config):
    producer = DummyProducer()
    producer.register()
    consumer = DummyConsumer()
    consumer.consume()
