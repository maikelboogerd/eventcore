import abc

from .exceptions import NoProducerError
from .registry import Registry


class Event(metaclass=abc.ABCMeta): # noqa
    """
    Event base class to create custom events from.
    :param subject: identifier for resource.
    :param data: dictionary with context for this event.
    """
    topic = None
    name = None

    def __init__(self, subject, data={}):
        self.subject = subject
        self.data = data

    def dispatch(self, producer=None):
        """
        Dispatch the event, sending a message to the queue using a producer.
        :param producer: optional `Producer` to replace the default one.
        """
        producer = (producer or Registry.get_producer())
        if not producer:
            raise NoProducerError('You have not configured a Producer')
        producer.produce(self.topic, self.name, self.subject, self.data)
