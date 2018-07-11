class Registry(object):
    """
    A simple registry to save classes and objects on.
    """
    _events = {}
    _producer = None

    @classmethod
    def register_event(cls, event_name, event, method):
        """
        Register an event class on it's name with a method to process it.
        :param event_name: name of the event.
        :param event: class of the event.
        :param method: a method used to process this event.
        """
        if event_name not in cls._events:
            cls._events[event_name] = (event, [])
        cls._events[event_name][1].append(method)

    @classmethod
    def register_producer(cls, producer):
        """
        Register a default producer for events to use.
        :param producer: the default producer to to dispatch events on.
        """
        cls._producer = (cls._producer or producer)

    @classmethod
    def get_event(cls, event_name):
        """
        Find the event class and registered methods.
        :param event_name: name of the event.
        """
        return cls._events.get(event_name, (None, []))

    @classmethod
    def get_producer(cls):
        """
        Get the default producer.
        """
        return cls._producer
