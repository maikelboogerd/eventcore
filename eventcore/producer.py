from .registry import Registry


class Producer(metaclass=abc.ABCMeta): # noqa
    @abc.abstractmethod
    def produce(self, topic, event, subject, data):
        """
        Send a message to the queue.
        :param topic: the topic the message is for.
        :param event: name of the event.
        :param subject: identifier for resource.
        :param data: dictionary with information for this event.
        """
        pass

    def register(self):
        """
        Add this producer to the `Registry` as default producer.
        """
        Registry.register_producer(self)
