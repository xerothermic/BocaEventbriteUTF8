from dataclasses import dataclass
from datetime import datetime

@dataclass
class CommonEventFields:
    """ Common event fields shared across ticket platforms """
    event_title: str
    event_start_datetime: datetime
    event_end_datetime: datetime
