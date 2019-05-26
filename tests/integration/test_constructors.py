import unittest

from mockito import mock

from eventcore.event import Event
from eventcore.dummy import DummyConsumer, DummyProducer


class TestConstructors(unittest.TestCase):
    """
    """

    def test_event_constructor(self):
        """
        Check if the `Event` subclass can be initialized.
        """
        class SomeEvent(Event):
            topic = 'some-topic'

        try:
            SomeEvent('a-subject', {'name': 'a-name'})
        except:
            self.fail('Cannot initialize `Event` subclass with known params')

    def test_dummy_consumer_constructor(self):
        """
        Check if the `DummyConsumer` can be initialized.
        """
        try:
            DummyConsumer()
        except:
            self.fail('Cannot initialize `DummyConsumer` with known params')

    def test_dummy_producer_constructor(self):
        """
        Check if the `DummyProducer` can be initialized.
        """
        try:
            DummyProducer()
        except:
            self.fail('Cannot initialize `DummyProducer` with known params')
