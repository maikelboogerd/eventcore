import unittest

from eventcore import Event, DummyProducer, DummyQueue


class DummyEvent(Event):
    name = 'DummyEvent'
    topic = 'dummy'


class TestEvent(unittest.TestCase):
    """
    """

    A_SUBJECT = 'a-subject'
    A_DATA_DICT = {'test': 'a-test'}

    def setUp(self):
        """
        """
        self.producer = DummyProducer()
        self.event = DummyEvent(self.A_SUBJECT, self.A_DATA_DICT)

    def tearDown(self):
        """
        """
        pass

    def test_subject(self):
        """
        """
        self.assertEqual(self.event.subject, self.A_SUBJECT)

    def test_data(self):
        """
        """
        self.assertEqual(self.event.data, self.A_DATA_DICT)

    def test_dispatch(self):
        """
        """
        self.event.dispatch(self.producer)
        self.assertEqual(len(DummyQueue._messages), 1)

    def test_discover_topics(self):
        """
        """
        result = Event.discover_topics()
        self.assertEqual(result, [DummyEvent.topic])
