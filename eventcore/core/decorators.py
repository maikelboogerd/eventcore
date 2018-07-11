from .registry import Registry


def event_subscriber(event):
    """
    Register a method, which gets called when this event triggers.
    :param event: the event to register the decorator method on.
    """
    def wrapper(method):
        Registry.register_event(event.name, event, method)
    return wrapper


def dispatch_event(event, subject='id', serializer=None):
    """
    Dispatch an event when the decorated method is called.
    :param event: the event class to instantiate and dispatch.
    :param subject_property: the property name to get the subject.
    """
    def wrapper(method):
        def inner_wrapper(*args, **kwargs):
            resource = method(*args, **kwargs)
            event(getattr(resource, subject), {}).dispatch()
            return resource
        return inner_wrapper
    return wrapper
