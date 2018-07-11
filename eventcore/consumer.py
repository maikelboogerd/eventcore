from contextlib import suppress


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

    def set_context_manager(self, context_manager):
        """
        Add a context manager to wrap event processing.
        :param context_manager: the context manager to use.
        """
        self._context_manager = context_manager

    def process_event(self, name, subject, data):
        """
        Process a single event.
        :param name:
        :param subject:
        :param data:
        """
        with self._context_manager:
            # Find the event and methods in the `Registry`.
            event, methods = Registry.get_event(name)
            # Return when the registry cannot find a match.
            if not (event and methods):
                return
            # Execute each registered method for this event.
            event_instance = event(subject, data)
            for method in methods:
                method(event_instance)

    def thread(self):
        """
        Start a thread for this consumer.
        """
        pass
