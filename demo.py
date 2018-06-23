import logging

from eventbus import (Consumer,
                      Producer,
                      Event,
                      event_subscriber,
                      dispatch_event)
from eventbus.queues import DummyQueue

log = logging.getLogger(__name__)


class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'


@event_subscriber(UserCreated)
def process_user_created(event):
    print('> @process_user_created {}'.format(event.subject))
    pass


@event_subscriber(UserCreated)
def do_something(event):
    print('> @do_something {}'.format(event.subject))
    pass


class User(object):
    id = '123'
    name = 'Maikel'


class SomeService(object):
    @dispatch_event(UserCreated)
    def create_user(self, id, data=None):
        return User()


if __name__ == '__main__':
    queue = DummyQueue()
    producer = Producer(queue) # noqa
    consumer = Consumer(queue)
    # UserCreated('123', {}).dispatch()
    # UserCreated('123', {}).dispatch()
    # UserCreated('123', {}).dispatch()
    # UserCreated('123', {}).dispatch()
    # UserCreated('123', {}).dispatch()
    user = SomeService().create_user('123', {})
    print(user)
    UserCreated('123', {}).dispatch()
    # consumer.consume()
