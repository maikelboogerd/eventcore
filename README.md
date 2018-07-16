# eventcore

Produce and consume events with any queue.

## Installation

This project is hosted on PyPI and can be installed with pip:

```
$ pip install eventcore
```

This only includes a (local) dummy queue, which can be used for testing or development environments. In the usage section some examples are shown on how to use this library with Kafka or SQS, which are more suited for production systems.

## Usage

Produce events:

```python
from eventcore import Event, DummyProducer, dispatch_event

# Implemented `Event` for the creation of a user.
class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'

# Create a `DummyProducer` and register as the default producer.
producer = DummyProducer()
producer.register()

# Create a `UserCreated` object with a subject and data.
# The event is dispatched using the default producer when calling `dispatch`.
UserCreated('cfce9306-3b33-4cb2-a51f-9dc4879cc7a2', {}).dispatch()

@dispatch_event(UserCreated)
def create_user(params):
    # Each time this method is called, the `UserCreated` event is created and
    # dispatched using the resource this method returns as context.
    # The returned object has the subject extracted from it, which uses `id`
    # property as default. This can be overwritten with the subject param on
    # the `dispatch_event` decorator.
    user = User(**params)
    return user
```

Consume events:

```python
from eventcore import Event, DummyConsumer, event_subscriber

# Implemented `Event` for the creation of a user.
class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'

@event_subscriber(UserCreated)
def send_activation(event):
    # This method is executed whenever the consumer return the `UserCreated`
    # event from the queue. You can register multiple methods as subscriber
    # by using the `event_subscriber` decorator like this example shows.
    pass

# Start consuming and processing the queue.
consumer = DummyConsumer()
consumer.thread()
```

Usage with Kafka:

```
$ pip install eventcore-kafka
```

```python
from eventcore_kafka import KafkaProducer

producer = KafkaProducer(servers='localhost:9092')
producer.register()
```

```python
from eventcore_kafka import KafkaProducer

consumer = KafkaConsumer(servers='localhost:9092',
                         group_id='user_service',
                         topics='user')
consumer.thread()
```

Usage with SQS:

```
$ pip install eventcore-kafka
```

```python
from eventcore_sqs import SQSProducer

producer = SQSProducer(region_name='eu-west-1',
                       access_key_id='ACCESS_KEY_ID',
                       secret_access_key='SECRET_ACCESS_KEY',
                       url='https://.../example.fifo')
producer.register()
```

```python
from eventcore_sqs import SQSConsumer

consumer = SQSConsumer(region_name='eu-west-1',
                       access_key_id='ACCESS_KEY_ID',
                       secret_access_key='SECRET_ACCESS_KEY',
                       url='https://.../example.fifo')
consumer.thread()
```
