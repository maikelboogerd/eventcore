class ProducerError(Exception):
    """
    Exception is thrown when producing fails.
    """
    pass


class MissingProducerError(ProducerError):
    """
    Exception is thrown when trying to dispatch without a producer.
    """
    pass


class ConsumerError(Exception):
    """
    Exception is thrown when consuming fails.
    """
    pass


class FatalConsumerError(ConsumerError):
    """
    Exception is thrown when consuming fails and is irrecoverable.
    """
    pass

