import logging

from eventcore.consumer import Consumer
from .queue import DummyQueue

log = logging.getLogger(__name__)


class DummyConsumer(Consumer):
    """
    Consume from a dummy queue.
    """

    def consume(self):
        """
        Retrieve message and trigger `process_event` on every message returned.
        """
        while True:
            self.sleep()
            for message in DummyQueue.read():
                try:
                    self.process_event(name=message.event,
                                       subject=message.subject,
                                       data=message.data)
                    DummyQueue.remove(message)
                except:
                    log.error('@DummyConsumer.consume Exception:',
                              exc_info=True)
                    continue
