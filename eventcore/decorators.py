import logging

from .registry import Registry

log = logging.getLogger(__name__)


def event_subscriber(event):
    """
    Register a method, which gets called when this event triggers.
    :param event: the event to register the decorator method on.
    """
    def wrapper(method):
        Registry.register_event(event.name, event, method)
    return wrapper


def dispatch_event(event, subject='id'):
    """
    Dispatch an event when the decorated method is called.
    :param event: the event class to instantiate and dispatch.
    :param subject: the property name to get the subject.
    """
    def wrapper(method):
        def inner_wrapper(*args, **kwargs):
            resource = method(*args, **kwargs)
            if isinstance(resource, dict):
                subject_ = resource.get(subject)
                data = resource
            else:
                subject_ = getattr(resource, subject)
                data = resource.__dict__
            event(subject_, data).dispatch()
            return resource
        return inner_wrapper
    return wrapper
