# eventcore

[![Build Status](https://travis-ci.com/maikelboogerd/eventcore.svg?branch=master)](https://travis-ci.com/maikelboogerd/eventcore)

Produce and consume events with any queue.

## Installation

This project is hosted on PyPI and can be installed with pip:

```
$ pip install eventcore
```

The default installation includes a `DummyProducer` and `DummyConsumer` that can be used for testing or development environments.

**For production systems you should use either [Kafka](#feature---kafka) or [SQS](#feature---sqs) included in this library.**

## Usage

### Configure a Producer

Before you can dispatch events you need to register a default producer, this could be changed depending on the type of queue you want to use. The producer implements a persistence mechanism that is used whenever `dispatch()` gets called.

```python
from eventcore.dummy import DummyProducer

producer = DummyProducer()
producer.register()
```

> The producer from this example stores your events in memory and is reset when the current process ends.

### Configure a Consumer

In order to retrieve events you'll need to create and run a consumer instance. The consumer will stay active in a separate thread to keep listening for new events by calling `thread()` on it.

```python
from eventcore.dummy import DummyConsumer

consumer = DummyConsumer()
consumer.thread()
```

### Events

Create your own events using `Event` as base class. These custom events must set the properties topic and name as is shown in the example.

```python
from eventcore import Event

class UserCreated(Event):
    topic = 'User'
    name = 'UserCreated'
```

### Dispatching

Events can be instantiated and dispatched on the fly. Doing so requires you to pass the subject and data arguments. Call `dispatch()` on the event to have your default producer store it.

```python
event = UserCreated(subject='cfce9306-3b33-4cb2-a51f-9dc4879cc7a2'
                    data={'name': 'John Doe'})
event.dispatch()
```

Alternatively, you can dispatch events whenever a method is called by using the `dispatch_event` decorator. This uses the return value of the decorated method to build the event instance. When the return value is a non-dictionary object, it uses it's `__dict__` property to populate event data.

```python
from eventcore import dispatch_event

@dispatch_event(UserCreated, subject='id')
def create_user():
    user = User(name='John Doe')
    return user
```

### Subscribers

Whenever your consumer retrieves new events it will execute all subscriber methods registered for it, passing the event instance as the only argument.

```python
from eventcore import event_subscriber

@event_subscriber(UserCreated)
def send_activation(event):
    pass
```

## Utility

### Context managers

Add a context manager that wraps around the execution of each `event_subscriber`. This could be used to manage database transactions.

```python
import transaction

consumer = DummyConsumer()
consumer.set_context_manager(transaction.manager)
consumer.thread()
```

### Multiple producers

You can bypass the default producer by passing a alternative one to the `dispatch()` method. This could allow you to use e.g. Kafa as a default, while still sending some specific events to SQS.

```
from eventcore.dummy import DummyProducer

alternative_producer = DummyProducer()
event.dispatch(alternative_producer)
```

## Feature - Kafka

Installation is **only required** if you want to use the `eventcore_kafka` package.

> This install includes the library `confluent-kafka`

```
$ pip install eventcore-kafka
```

The below examples show the different configuration needed for the producer and consumer when using Kafka.

```python
from eventcore_kafka import KafkaProducer

producer = KafkaProducer(servers='localhost:9092')
producer.register()
```

```python
from eventcore_kafka import KafkaConsumer

consumer = KafkaConsumer(servers='localhost:9092',
                         group_id='user_service',
                         topics='user')
consumer.thread()
```

## Feature - SQS

Installation is **only required** if you want to use the `eventcore.sqs` package.

> This install includes the library `boto3==1.9.*`

```
$ pip install eventcore[sqs]
```

The below examples show the different configuration needed for your producer and consumer when using SQS.

```python
from eventcore.sqs import SQSProducer

producer = SQSProducer(region_name='eu-west-1',
                       access_key_id='ACCESS_KEY_ID',
                       secret_access_key='SECRET_ACCESS_KEY',
                       queue_url='https://.../example.fifo')
producer.register()
```

```python
from eventcore.sqs import SQSConsumer

consumer = SQSConsumer(region_name='eu-west-1',
                       access_key_id='ACCESS_KEY_ID',
                       secret_access_key='SECRET_ACCESS_KEY',
                       queue_url='https://.../example.fifo')
consumer.thread()
```