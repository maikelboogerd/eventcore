import abc
import threading
import logging

from contextlib import suppress

from .registry import Registry

log = logging.getLogger(__name__)


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
            log.warning('@{}.process_event no subscriber for event `{}`'
                        .format(self.__class__.__name__, name))
            return
        event_instance = event(subject, data)
        log.info('@{}.process_event `{}` for subject `{}`'
                 .format(self.__class__.__name__, event, subject))
        for method in methods:
            log.info('>> Calling subscriber `{}`'.format(method.__name__))
            method(event_instance)

    def thread(self):
        """
        Start a thread for this consumer.
        """
        log.info('@{}.thread starting'.format(self.__class__.__name__))
        thread = threading.Thread(target=thread_wrapper(self.consume), args=())
        thread.daemon = True
        thread.start()


def thread_wrapper(method):
    def wrapper():
        while True:
            try:
                method()
            except BaseException as e:
                log.error('@thread_wrapper restarting thread after exception:',
                          exc_info=True)
                continue
    return wrapper
