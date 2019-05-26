import unittest

from mockito import mock

from eventcore.event import Event
from eventcore.dummy import DummyProducer, DummyQueue


class TestEvent(unittest.TestCase):
    """
    """

    A_SUBJECT = 'a-subject'
    A_EVENT = mock({
        'name': 'a-name',
        'topic': 'a-topic',
        'subject': A_SUBJECT,
        'data': 'a-data'
    }, spec=Event)

    def setUp(self):
        """
        """
        self.producer = DummyProducer()

    def test_dispatch(self):
        """
        Check if our mock event ends up in our queue when `dispatch` is called.
        """
        Event.dispatch(self.A_EVENT, self.producer)
        self.assertEqual(len(DummyQueue._messages), 1)

    def test_discover_topics(self):
        """
        Check if the base `Event` can detect all defined subclasses and return
        their unique topics.
        """
        class SomeEvent(Event):
            topic = 'some-topic'

        class AnotherEvent(Event):
            topic = 'another-topic'

        result = Event.discover_topics()
        self.assertEqual(len(result), 2)
        self.assertTrue(SomeEvent.topic in result)
        self.assertTrue(AnotherEvent.topic in result)
