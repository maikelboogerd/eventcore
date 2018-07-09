from eventcore import Queue, Message


class DummyQueue(Queue):
    _queue = []

    def read(self, topics=None):
        for message in self._queue:
            yield message

    def enqueue(self, message):
        self._queue.append(message)

    def dequeue(self, message):
        self._queue.remove(message)

    def prepare(self, topic, event, subject, data):
        return DummyMessage(topic, event, subject, data)


class DummyMessage(Message):
    pass
