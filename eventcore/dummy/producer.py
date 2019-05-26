from eventcore.producer import Producer

from .queue import DummyQueue, DummyMessage


class DummyProducer(Producer):
    """
    Produce to a dummy queue.
    """

    def produce(self, topic, event, subject, data):
        """
        Add a message to the `DummyQueue`.
        :param topic: the topic the message is for.
        :param event: name of the event.
        :param subject: identifier for resource.
        :param data: dictionary with information for this event.
        """
        message = DummyMessage(topic, event, subject, data)
        DummyQueue.add(message)
