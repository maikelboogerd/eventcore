import abc

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
        default_producer = Registry.get_producer()
        (producer or default_producer).produce(self.topic,
                                               self.name,
                                               self.subject,
                                               self.data)
