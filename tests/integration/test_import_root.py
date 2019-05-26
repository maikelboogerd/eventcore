import unittest

from mockito import mock


class TestImportRoot(unittest.TestCase):
    """
    """

    def test_import_consumer(self):
        """
        Try to import the `eventcore.Consumer`.
        """
        try:
            from eventcore import Consumer
        except ImportError:
            self.fail('Cannot import `Consumer`')

    def test_import_event_subscriber(self):
        """
        Try to import the `eventcore.event_subscriber`.
        """
        try:
            from eventcore import event_subscriber
        except ImportError:
            self.fail('Cannot import `event_subscriber`')

    def test_import_dispatch_event(self):
        """
        Try to import the `eventcore.dispatch_event`.
        """
        try:
            from eventcore import dispatch_event
        except ImportError:
            self.fail('Cannot import `dispatch_event`')

    def test_import_event(self):
        """
        Try to import the `eventcore.Event`.
        """
        try:
            from eventcore import Event
        except ImportError:
            self.fail('Cannot import `Event`')

    def test_import_dummy_consumer(self):
        """
        Try to import the `eventcore.DummyConsumer`.
        """
        try:
            from eventcore import DummyConsumer
        except ImportError:
            self.fail('Cannot import `DummyConsumer`')

    def test_import_dummy_producer(self):
        """
        Try to import the `eventcore.DummyProducer`.
        """
        try:
            from eventcore import DummyProducer
        except ImportError:
            self.fail('Cannot import `DummyProducer`')
