class NoProducerError(Exception):
    """
    Exception is thrown when trying to dispatch without a producer.
    """
    pass
