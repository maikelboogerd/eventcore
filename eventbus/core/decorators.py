from .registry import Registry


def event_subscriber(event):
    """
    Register a method, which gets called when this event triggers.
    :param event: the event to register the decorator method on.
    """
    def wrapper(method):
        Registry.register_event(event.name, event, method)
    return wrapper


def dispatch_event(event):
    """
    Dispatch an event when the decorated method is called.
    :param event: the event class to instantiate and dispatch.
    """
    def wrapper(method):
        def inner_wrapper(*args, **kwargs):
            resource = method(*args, **kwargs)
            subject = getattr(resource, 'id')
            event(subject, {}).dispatch()
            return resource
        return inner_wrapper
    return wrapper
