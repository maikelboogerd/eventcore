import unittest

from mockito import mock

from eventcore.event import Event
from eventcore.producer import Producer
from eventcore.registry import Registry


class TestRegistry(unittest.TestCase):
    """
    """

    A_EVENT = mock({'name': 'a-name'}, spec=Event)
    A_PRODUCER = mock(spec=Producer)
    A_FALLBACK = mock()

    def setUp(self):
        """
        """
        self.registry = Registry

    def test_register_event(self):
        """
        Try to register an event and retrieve it.
        """
        self.registry.register_event(self.A_EVENT.name,
                                     self.A_EVENT,
                                     lambda: True)
        result = self.registry.get_event(self.A_EVENT.name)
        self.assertEqual(len(result), 1)
        result = next(iter(result))
        self.assertEqual(result, self.A_EVENT)

    def test_register_producer(self):
        """
        Try to register a producer and retrieve it.
        """
        self.registry.register_producer(self.A_PRODUCER)
        result = self.registry.get_producer()
        self.assertEqual(result, self.A_PRODUCER)

    def test_register_fallback(self):
        """
        Try to register a fallback method and retrieve it.
        """
        self.registry.register_fallback(self.A_FALLBACK)
        result = self.registry.get_fallback()
        self.assertEqual(result, self.A_FALLBACK)
