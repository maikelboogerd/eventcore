from eventcore import Queue, Message


class KafkaQueue(Queue):
    def read(self, topic=None):
        pass

    def enqueue(self, message):
        pass

    def dequeue(self, message):
        pass

    def prepare(self, topic, event, subject, data):
        return KafkaMessage(topic, event, subject, data)


class KafkaMessage(Message):
    pass
