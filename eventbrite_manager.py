import sys
from eventbrite import Eventbrite
import logging
import os

from data_model import gen_obj

logger = logging.getLogger(__name__)

class EventbriteManager(object):
    """ Handle Eventbrite API calls for specific event """
    def __init__(self) -> None:
        self._check_token()
        self._conn = Eventbrite(os.environ.get('EVENTBRITE_TOKEN'))

    def _unused_only(self, unused_only: bool, attendee: dict) -> bool:
        return not unused_only or attendee['barcodes'][0]['status'] == 'unused'
    
    def _filter_unused_attendees(self, unused_only: bool, attendees: list) -> list:
        return filter(lambda p: self._unused_only(unused_only, p), attendees)
    
    def _map_attendees_with_assigned_units(self, attendees: list) -> list:
        return map(lambda p: self._get_attendee_by_id(p['event_id'], p['id']), attendees)

    def _check_token(self):
        if 'EVENTBRITE_TOKEN' not in os.environ:
            logger.error("Please set the environment variable EVENTBRITE_TOKEN to your Eventbrite API token")
            sys.exit(1)

    def _get_attendee_by_id(self, event_id, attendee_id):
        return self._conn.get(f'/events/{event_id}/attendees/{attendee_id}/', {'expand': 'assigned_unit'})

    def get_attendees_by_order_id(self, order_id: int, unused_only: bool = True):
        resp = self._conn.get(f'/orders/{order_id}/', {'expand': 'attendees'})
        if 'attendees' not in resp: # type: ignore
            return []

        attendees = self._filter_unused_attendees(unused_only, resp['attendees']) # type: ignore
        attendees_with_assigned_units = self._map_attendees_with_assigned_units(attendees)
        yield from map(gen_obj, attendees_with_assigned_units)

    def get_attendees_by_event_id(self, event_id: int, unused_only: bool = True):
        resp = self._conn.get(f'/events/{event_id}/attendees/', {'expand': 'assigned_unit'})
        pagination, attendees = resp['pagination'], resp['attendees'] # type: ignore
        attendees = self._map_attendees_with_assigned_units(self._filter_unused_attendees(unused_only, attendees))
        yield from map(gen_obj, attendees)
        while pagination['has_more_items']:
            resp = self._conn.get(f'/events/{event_id}/attendees/', {'continuation': pagination['continuation']})
            pagination, attendees = resp['pagination'], resp['attendees'] # type: ignore
            attendees = self._map_attendees_with_assigned_units(self._filter_unused_attendees(unused_only, attendees))
            yield from map(gen_obj, attendees)

    def get_event_detail(self, event_id: int):
        return gen_obj(self._conn.get(f'/events/{event_id}/', {'expand': 'venue,organizer'}))

    def get_ticket_class_detail(self, event_id: int, ticket_class_id: int):
        return gen_obj(self._conn.get_event_ticket_class_by_id(event_id, ticket_class_id))

if __name__ == "__main__":
    logging.basicConfig()

    EVENT_ID = 579945642027
    ebm = EventbriteManager()
    attendees = ebm.get_attendees_by_event_id(EVENT_ID)
    for p in attendees:
        logger.debug(p.profile.name, p.id, p.order_id, p.barcodes[0].status, p.barcodes[0].barcode, p.barcodes[0].is_printed, p.assigned_unit.pairs)

    event = ebm.get_event_detail(EVENT_ID)
    logger.debug(event.name.text, event.start.local, event.end.local, event.venue.address.localized_address_display)