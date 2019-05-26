import unittest

from eventcore.dummy import DummyConsumer


class TestConsumer(unittest.TestCase):
    """
    """

    A_CONTEXT_MANAGER = 'a-context-manager'

    def setUp(self):
        """
        """
        self.consumer = DummyConsumer()

    def test_set_context_manager(self):
        """
        Check if the context manager is saved on the consumer.
        """
        self.consumer.set_context_manager(self.A_CONTEXT_MANAGER)
        self.assertEqual(self.consumer._context_manager,
                         self.A_CONTEXT_MANAGER)
