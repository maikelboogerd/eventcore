import unittest

from eventcore import DummyConsumer


class TestConsumer(unittest.TestCase):
    """
    """

    A_CONTEXT_MANAGER = 'a-context-manager'

    def setUp(self):
        """
        """
        self.consumer = DummyConsumer()

    def tearDown(self):
        """
        """
        pass

    def test_set_context_manager(self):
        """
        """
        self.consumer.set_context_manager(self.A_CONTEXT_MANAGER)
        self.assertEqual(self.consumer._context_manager,
                         self.A_CONTEXT_MANAGER)
