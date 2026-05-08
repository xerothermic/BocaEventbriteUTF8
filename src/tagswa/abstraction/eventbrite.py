from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Optional

@dataclass
class EventbriteAttendee:
    """ Eventbrite attendee data extracted from the attendees API """
    profile_name: str           # profile.name
    barcode: str                # barcodes[0].barcode
    price_display: str          # costs.gross.display
    order_id: str               # order_id
    event_id: str               # event_id
    ticket_class_id: str        # used by main.py to call get_ticket_class_detail()
    ticket_class_name: str      # displayed on ticket stub via _place_ticket_class()
    assigned_unit_pairs: list = field(default_factory=list)  # seat assignments for _place_seat_details()
    ticket_description: Optional[str] = None  # injected later in main.py after get_ticket_class_detail()

    @classmethod
    def from_attendee_api(cls, ns: SimpleNamespace) -> "EventbriteAttendee":
        """ Create EventbriteAttendee from Eventbrite API SimpleNamespace """
        pairs = []
        if hasattr(ns, 'assigned_unit') and hasattr(ns.assigned_unit, 'pairs'):
            pairs = ns.assigned_unit.pairs

        return cls(
            profile_name=ns.profile.name,
            barcode=str(ns.barcodes[0].barcode),
            price_display=ns.costs.gross.display,
            order_id=str(ns.order_id),
            event_id=str(ns.event_id),
            ticket_class_id=str(ns.ticket_class_id),
            ticket_class_name=ns.ticket_class_name,
            assigned_unit_pairs=pairs,
            ticket_description=getattr(ns, 'ticket_description', None),
        )
