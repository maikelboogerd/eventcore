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

queue = DummyQueue()
producer = Producer(queue)
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

Dispatching events can be done in two ways, providing some flexibility:
- Using the `dispatch_event` decorator an event is dispatched when the method is called, using the resource it returns as context.
- Alternatively you can dispatch events yourself by instantiating the event with a subject and dictionary. Call `.dispatch()` on it to persist it to a queue.

```python
from eventcore import dispatch_event
from project.events import UserCreated, UserUpdated

class User(object):
    pass

class UserService(object):
    @dispatch_event(UserCreated)
    def create(self):
        return User()

    def update(self):
        UserUpdated('USER_ID', {}).dispatch()
```
