import time
import threading
import logging

from contextlib import suppress

from .registry import Registry

log = logging.getLogger(__name__)


class Consumer(object):
    """
    Consume messages from a queue.
    :param queue: the `Queue` instance to read messages from.
    """
    _interval = 5

    def __init__(self, queue, context_manager=None):
        self._queue = queue
        self._context_manager = (context_manager or suppress())

    def process_queue(self):
        """
        Read and process messages from the queue.
        """
        for message in self._queue.read():
            try:
                # Wrap a transaction manager around the message processing
                # so each message has it's own session. Upon completing the
                # message processing everything is persisted to the database.
                with self._context_manager:
                    self.process_message(message)
            except:
                # Log the exception on error level, but continue processing
                # other queue messages.
                log.error('Exception occured while processing message',
                          exc_info=True)
                continue

    def process_message(self, message):
        """
        Process a single message and execute the registered methods.
        :param message: the `Message` to be processed.
        """
        # Find the event and methods in the `Registry`.
        event, methods = Registry.get_event(message.event)
        # Return when the registry cannot find a match.
        if not (event and methods):
            return
        # Execute each registered method for this event.
        event_instance = event(message.subject, message.data)
        for method in methods:
            method(event_instance)
        # Remove the message when it's fully processed.
        self._queue.dequeue(message)

    def consume(self):
        """
        Runs `process_queue` on loop until the process is killed.
        """
        while True:
            self.process_queue()
            time.sleep(self._interval)

    def thread(self):
        """
        Start a thread for the `consume` method.
        """
        thread = threading.Thread(target=self.consume, args=())
        thread.daemon = True
        thread.start()
