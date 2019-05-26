import unittest

from mockito import mock


class TestImportException(unittest.TestCase):
    """
    """

    def test_producer_error(self):
        """
        Try to import the `eventcore.exceptions.ProducerError`.
        """
        try:
            from eventcore.exceptions import ProducerError
        except ImportError:
            self.fail('Cannot import `exceptions.ProducerError`')

    def test_missing_producer_error(self):
        """
        Try to import the `eventcore.exceptions.ProducerError`.
        """
        try:
            from eventcore.exceptions import MissingProducerError
        except ImportError:
            self.fail('Cannot import `exceptions.MissingProducerError`')

    def test_consumer_error(self):
        """
        Try to import the `eventcore.exceptions.ProducerError`.
        """
        try:
            from eventcore.exceptions import ConsumerError
        except ImportError:
            self.fail('Cannot import `exceptions.ConsumerError`')

    def test_fatal_consumer_error(self):
        """
        Try to import the `eventcore.exceptions.ProducerError`.
        """
        try:
            from eventcore.exceptions import FatalConsumerError
        except ImportError:
            self.fail('Cannot import `exceptions.FatalConsumerError`')

    def test_missing_dependency_error(self):
        """
        Try to import the `eventcore.exceptions.ProducerError`.
        """
        try:
            from eventcore.exceptions import MissingDependencyError
        except ImportError:
            self.fail('Cannot import `exceptions.MissingDependencyError`')
