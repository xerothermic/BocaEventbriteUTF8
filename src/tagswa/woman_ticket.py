import logging
from typing import List

from tagswa.meydenbauer_ticket import TaiwanAcrobaticTroupeTicket

logger = logging.getLogger(__name__)


class WomanTicket(TaiwanAcrobaticTroupeTicket):
    """ WC """
    EVENTID = "885391679347"

    def _gen_fgl_script_from_ns(self) -> List[str]:
        strings = []
        logger.debug("_place_org_title")
        self._place_org_title(strings)
        self._place_event_title(strings)
        self._place_venue_info(strings)
        self._place_event_time(strings)
        # self._place_price(strings)
        self._place_attendee_name(strings)
        # self._place_seat_details_long(strings)
        self._place_ticket_description(strings)
        self._place_order_id(strings)
        self._place_ticket_class(strings)
        # self._place_seat_details_short(strings)
        self._place_barcode(strings)
        # self._place_tags_logo_2x(strings)

        self._place_cut_cmd(strings)
        return strings
