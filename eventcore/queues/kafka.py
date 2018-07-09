import json

from eventcore import Queue, Message
from confluent_kafka import Producer, Consumer


class KafkaQueue(Queue):
    def __init__(self, server, group_id=None):
        self.kafka_producer = Producer({'bootstrap.servers': server})
        if group_id:
            self.kafka_consumer = Consumer({
                'bootstrap.servers': server,
                'group.id': group_id
            })

    def read(self, topics=None):
        self.kafka_consumer.subscribe(topics)
        for resource in self.kafka_consumer.consume(10, 1):
            if not resource:
                continue
            message_body = json.loads(resource.value())
            message = self.prepare(topic=resource.topic(),
                                   event=message_body.get('event'),
                                   subject=resource.key(),
                                   data=message_body.get('data'))
            yield message

    def enqueue(self, message):
        message_body = {
            'event': message.event,
            'data': message.data
        }
        self.kafka_producer.produce(message.topic,
                                    key=message.subject,
                                    value=json.dumps(message_body))
        self.kafka_producer.flush()

    def dequeue(self, message):
        # Not available in Kafka
        pass

    def prepare(self, topic, event, subject, data):
        return KafkaMessage(topic, event, subject, data)


class KafkaMessage(Message):
    pass
