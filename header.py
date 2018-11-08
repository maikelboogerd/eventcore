import datetime
import uuid


class Header:
    """
    Provides the meta information needed to increase traceability.
    """

    id = ''
    source = ''
    timestamp = ''
    type = ''

    def __init__(self, source=None, event=None):
        """
        Id and timestamps are added automatically. The id is an UUID which
        identifies the current message, so it can be traced across services.
        :param source: The source which the message is originated from.
        :param event: The name of the event which is produced.
        """
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.datetime.now().isoformat()
        self.source = source
        self.type = event

