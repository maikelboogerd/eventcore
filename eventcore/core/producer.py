from .registry import Registry


class Producer(object):
    """
    Produce messages and put them in a queue.
    :param queue: the `Queue` instance to send messages to.
    """

    def __init__(self, queue):
        self._queue = queue
        # Add the first producer as the default one to the registry.
        if not Registry.get_producer():
            Registry.register_producer(self)

    def produce(self, topic, event, subject, data):
        """
        Send a `Message` to the `Queue`.
        :param topic: the topic the message is for.
        :param event: name of the event.
        :param subject: identifier for resource.
        :param data: dictionary with information for this event.
        """
        message = self._queue.prepare(topic=topic,
                                      event=event,
                                      subject=subject,
                                      data=data)
        self._queue.enqueue(message)
