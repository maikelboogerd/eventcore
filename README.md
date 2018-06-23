# python-eventcore

Produce and consume events with any queue.

## Installation

This project is hosted on PyPI and can be installed with pip:

```
$ pip install eventcore
```

## Usage

- Create a producer and consumer for a specific queue:

```python
from eventcore.queues import DummyQueue

queue = DummyQueue()
producer = Producer(queue)
consumer = Consumer(queue)
consumer.thread()
```

- Create events and register processors:

```python
from eventcore import Event, event_subscriber

class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'

@event_subscriber(UserCreated)
def send_activation(event):
    pass
```

- Dispatch events from your project:

```python
from eventcore import dispatch_event
from project.events import UserCreated

class User(object):
    pass

class UserService(object):
    @dispatch_event(UserCreated)
    def create(self):
        return User()
```
