import abc
import threading

from contextlib import suppress

from .registry import Registry


class Consumer(metaclass=abc.ABCMeta): # noqa
    """
    Consumer base to read messages from any queue.
    """
    _context_manager = suppress()

    @abc.abstractmethod
    def consume(self):
        """
        Consume from a queue.
        """
        pass

    def process_event(self, name, subject, data):
        """
        Process a single event.
        :param name:
        :param subject:
        :param data:
        """
        event, methods = Registry.get_event(name)
        if not (event and methods):
            return
        event_instance = event(subject, data)
        for method in methods:
            method(event_instance)

    def thread(self):
        """
        Start a thread for this consumer.
        """
        thread = threading.Thread(target=thread_wrapper(self.consume), args=())
        thread.daemon = True
        thread.start()


def thread_wrapper(method):
    def wrapper():
        while True:
            try:
                method()
            except BaseException as e:
                continue
    return wrapper
