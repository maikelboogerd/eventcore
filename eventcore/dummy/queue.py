class DummyQueue(object):
    """
    A simple queue that keeps messages stored in memory, this is queue is reset
    when the process is ended.
    """

    _messages = []

    @classmethod
    def add(cls, message):
        """
        Add a single message to the queue.
        :param message: the `DummyMessage instance to add.
        """
        cls._messages.append(message)

    @classmethod
    def read(cls):
        """
        Generator that returns the messages in our queue.
        """
        for message in cls._messages:
            yield message

    @classmethod
    def remove(cls, message):
        """
        Remove a single message from the queue.
        :param message: the `DummyMessage instance to remove.
        """
        cls._messages.remove(message)


class DummyMessage(object):
    """
    A simple message to store the event context in our queue.
    :param topic: the topic the message is for.
    :param event: name of the event.
    :param subject: identifier for resource.
    :param data: dictionary with information for this event.
    """

    def __init__(self, topic, event, subject, data):
        self.topic = topic
        self.event = event
        self.subject = subject
        self.data = data
