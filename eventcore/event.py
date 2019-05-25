import abc
import logging

from .exceptions import MissingProducerError
from .registry import Registry

log = logging.getLogger(__name__)


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
        log.info('@Event.dispatch `{}` with subject `{}`'
                 .format(self.name, self.subject))
        producer = (producer or Registry.get_producer())
        if not producer:
            raise MissingProducerError('You have not registered a Producer')
        try:
            producer.produce(self.topic, self.name, self.subject, self.data)
        except:
            fallback = Registry.get_fallback()
            fallback(self)
            raise

    @classmethod
    def get_topics(cls):
        """
        List all existing topics by checking the subclasses.
        """
        return [event.topic for event in cls.__subclasses__()]
