import abc
import threading
import logging
import time

from contextlib import suppress

from .exceptions import FatalConsumerError
from .registry import Registry

log = logging.getLogger(__name__)


class Consumer(metaclass=abc.ABCMeta): # noqa
    """
    Consumer base to read messages from any queue.
    """

    _interval = 0.5
    _context_manager = suppress()

    @abc.abstractmethod
    def consume(self):
        """
        Consume from a queue.
        """
        pass

    def set_context_manager(self, context_manager):
        """
        Wrap a context manager around subscriber execution.
        :param context_manager: object that implements __enter__ and __exit__
        """
        self._context_manager = context_manager

    def process_event(self, name, subject, data):
        """
        Process a single event.
        :param event: name of the event.
        :param subject: identifier for resource.
        :param data: dictionary with context for this event.
        """
        method_mapping = Registry.get_event(name)
        if not method_mapping:
            log.info('@{}.process_event no subscriber for event `{}`'
                     .format(self.__class__.__name__, name))
            return
        for event, methods in method_mapping.items():
            event_instance = event(subject, data)
            log.info('@{}.process_event `{}` for subject `{}`'.format(
                self.__class__.__name__,
                event_instance.__class__.__name__,
                subject
            ))
            for method in methods:
                with self._context_manager:
                    log.info('>> Calling subscriber `{}`'
                             .format(method.__name__))
                    method(event_instance)

    def sleep(self):
        """
        Sleep for the defined interval.
        """
        time.sleep(self._interval)

    def thread(self):
        """
        Start a thread for this consumer.
        """
        log.info('@{}.thread starting'.format(self.__class__.__name__))
        thread = threading.Thread(target=thread_wrapper(self.consume), args=())
        thread.daemon = True
        thread.start()


def thread_wrapper(method):
    """
    Wrapper that recovers a thread after an exception, but breaks
    when the `FatalConsumerError` is thrown.
    :param method: the decorated method that takes no arguments.
    """
    def wrapper():
        while True:
            try:
                method()
            except FatalConsumerError:
                raise
            except BaseException as e:
                log.error('@thread_wrapper restarting thread after Exception:',
                          exc_info=True)
                continue
    return wrapper
