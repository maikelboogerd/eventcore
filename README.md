# python-eventcore

Produce and consume events with any queue.

## Installation

This project is hosted on PyPI and can be installed with pip:

```
$ pip install eventcore
```

## Usage

Create a producer and consumer for a specific queue. This is best done once on application start.

```python
from eventcore.queues import DummyQueue

# Create a queue so we can produce/consume on it. This package supports queue
# implementations for SQS and Kafka as well as a dummy queue for testing.
queue = DummyQueue()

# The first producer you create will be used as the default for events
# to dispatch on.
producer = Producer(queue)

#
consumer = Consumer(queue)
consumer.thread()
```

Create events and subscribe methods that trigger when the event is returned from the queue.

```python
from eventcore import Event, event_subscriber

class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'

@event_subscriber(UserCreated)
def send_activation(event):
    pass
```

Dispatching events can be done in two ways:
- When using the `dispatch_event` decorator, the event is dispatched when the method is called.
- Alternatively you can dispatch events yourself by creating the event object and calling `.dispatch()` on it.

```python
from eventcore import dispatch_event
from project.events import UserCreated, UserUpdated

class UserService(object):
    @dispatch_event(UserCreated)
    def create(self):
        # Each time this method is called, the `UserCreated` event is created
        # and dispatched using the resource this method returns as context.
        return User()

    def update(self):
        # Dispatch the event to the default queue, which the `dispatch_event`
        # decorator does under the hood as well.
        UserUpdated('USER_ID', {}).dispatch()

        # You can pass a different Producer to dispatch this event to a
        # different queue instead.
        UserUpdated('USER_ID', {}).dispatch(Producer(SQSQueue()))
```
