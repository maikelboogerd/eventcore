import json

from eventcore import Queue, Message

from kafka import (KafkaConsumer,
                   KafkaProducer)


class KafkaQueue(Queue):
    def __init__(self,
                 server):
        self.kafka_consumer = KafkaConsumer(topic=self._topic,
                                            group_id=self._group_id,
                                            bootstrap_servers=[server])
        self.kafka_producer = KafkaProducer(topic=self._topic,
                                            group_id=self._group_id,
                                            bootstrap_servers=[server])

    def read(self, topic=None):
        # TODO: Remove confusing names within project (?)
        for resource in self.kafka_consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            message_value = json.loads(resource.value.decode('utf-8'))
            decoded_resource_key = resource.key.decode('utf-8')

            message = self.prepare(topic=None,
                                   event=message_value.get('event'),
                                   subject=message_value.get('subject'),
                                   data=message_value.get('data'))

            message.message_id = decoded_resource_key
            yield message

    def enqueue(self, message):
        pass

    def dequeue(self, message):
        pass

    def prepare(self, topic, event, subject, data):
        return KafkaMessage(topic, event, subject, data)


class KafkaMessage(Message):
    message_id = None
