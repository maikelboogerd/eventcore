import abc


class Queue(metaclass=abc.ABCMeta): # noqa
    """
    Base `Queue` to serve as interface for custom queues.
    """

    @abc.abstractmethod
    def read(self, topics=None):
        """
        Read messages from the queue.
        :param topic: the topic to read messages from.
        :param consumer_id: TODO
        :return messages: list of `Message` instances.
        """
        pass

    @abc.abstractmethod
    def enqueue(self, message):
        """
        Send a message to the queue.
        :param message: the `Message` to be sent.
        """
        pass

    @abc.abstractmethod
    def dequeue(self, message):
        """
        Remove a message from the queue.
        :param message: the `Message` to be removed.
        """
        pass

    def prepare(self, topic, event, subject, data):
        """
        Create a `Message` object.
        :param topic: the topic the message is for.
        :param event: name of the event.
        :param subject: identifier for resource.
        :param data: dictionary with context for this event.
        :return message: a `Message` instance.
        """
        return Message(topic, event, subject, data)


class Message(metaclass=abc.ABCMeta): # noqa
    """
    Message object to transfer data between producer, consumer and queue.
    :param topic: the topic the message is for.
    :param event: name of the event.
    :param subject: identifier for resource.
    :param data: dictionary with context for this event.
    """

    def __init__(self, topic, event, subject, data):
        self.topic = topic
        self.event = event
        self.subject = subject
        self.data = data
