from dataclasses import dataclass
from datetime import datetime

@dataclass
class CommonEventFields:
    """ Common Eventbrite event fields """
    org_title: str
    event_title: str
    venue_title: str
    venue_addr: str
    event_start_datetime: datetime
    event_end_datetime: datetime
