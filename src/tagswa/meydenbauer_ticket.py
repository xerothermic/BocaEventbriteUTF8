from tagswa.abstraction.ticket import Ticket
from tagswa.abstraction.event import CommonEventFields
from tagswa.abstraction.eventbrite import EventbriteAttendee
import re
import logging
from typing import List

logger = logging.getLogger(__name__)


class TaiwanAcrobaticTroupeTicket(Ticket):
    """ 傳統週特技團 """
    EVENTID = "579945642027"
    ORG_TITLE = "TAGS"
    VENUE_TITLE = "Meydenbauer Center"
    VENUE_ADDR = "11100 NE 6th St, Bellevue, WA 98004"

    def __init__(self, attendee: EventbriteAttendee, evf: CommonEventFields, ttf_font: str = "TTF1"):
        self._attendee = attendee
        self._ev_details = evf
        self._ttf_font = ttf_font

    def _gen_fgl_script_from_ns(self) -> List[str]:
        strings = []
        logger.debug("_place_org_title")
        self._place_org_title(strings)
        self._place_event_title(strings)
        self._place_venue_info(strings)
        self._place_event_time(strings)
        self._place_price(strings)
        # self._place_attendee_name(strings)
        self._place_seat_details_long(strings)
        self._place_ticket_description(strings)
        self._place_order_id(strings)
        self._place_ticket_class(strings)
        self._place_seat_details_short(strings)
        self._place_barcode(strings)
        # self._place_tags_logo_2x(strings)

        self._place_cut_cmd(strings)
        return strings

    def _place_cut_cmd(self, strings):
        strings.append("<p>")

    def _place_tags_logo(self, strings):
        strings.append("<SP425,1350><LD9>")

    def _place_tags_logo_2x(self, strings):
        strings.append("<HW2,2><SP275,1250><LD9>")

    def _place_barcode(self, strings):
        strings.append("<RC265,1500><QR5>" +
                       "{"+self._attendee.barcode+"}")
        strings.append(f"<RC505,1500><F2>{self._attendee.barcode}")

    def _place_seat_details_short(self, strings):
        seat_detail = [': '.join(pair)
                       for pair in self._attendee.assigned_unit_pairs]
        roff = 100
        for token in seat_detail:
            roff += 35
            strings.append(f"<RC{roff},1500>{token}")

    def _place_ticket_class(self, strings):
        roff = 10

        for l in Ticket.split_long_line(self._attendee.ticket_class_name, char_per_line=16):
            roff += 30
            strings.append(f"<RC{roff},1500>{l}")

    def _place_order_id(self, strings):
        # start again from the top row
        strings.append("<F3>")
        strings.append(f"<RC0,1200>#{self._attendee.order_id}")
        strings.append(f"<RC0,1500>#{self._attendee.order_id}")

    def _place_ticket_description(self, strings):
        if not self._attendee.ticket_description:
            return

        strings.append(
            f"<RC390,235><{self._ttf_font},8>{self._attendee.ticket_description}")

    def _place_seat_details_long(self, strings):
        """ Seat details on the long side (attendee keeps) """
        seat_detail = [': '.join(pair)
                       for pair in self._attendee.assigned_unit_pairs]
        strings.append("<RC490,65>{0}{1}{2}".format(
            self._attendee.ticket_class_name,
            ', ' if seat_detail else '',
            ', '.join(seat_detail)
        ))

    def _place_attendee_name(self, strings):
        strings.append(
            f"<RC440,65><{self._ttf_font},8>{self._attendee.profile_name}")

    def _place_price(self, strings):
        strings.append(f"<RC365,65>{self._attendee.price_display}")

    def _place_event_time(self, strings):
        strings.append("<RC315,65>{0} - {1}".format(
            self._ev_details.event_start_datetime.strftime('%c'),
            self._ev_details.event_end_datetime.strftime('%c')))

    def _place_venue_info(self, strings):
        strings.append("<F3>")
        strings.append(f"<RC215,65>{self.VENUE_TITLE}")
        strings.append(f"<RC265,65>{self.VENUE_ADDR}")

    def _place_event_title(self, strings):
        roff = 70

        strings.append(f"<{self._ttf_font},12>")
        # TTF1,12 pt font size is roughly 6漢字/inch. (50~60dots/漢字)
        # We have 4.75 inch of space, so 22 漢字 max。
        # However, alphabet takes less space, so in average, we can afford 30 per line.
        titles = Ticket.split_long_line(self._ev_details.event_title, 40)
        if len(titles) > 2:
            raise ValueError("Event title exceed two lines.")
        for title_fragment in titles:
            strings.append(f"<RC{roff},65>{title_fragment}")
            roff += 60

    def _place_org_title(self, strings):
        strings.append(
            f"<RC0,65><{self._ttf_font},8>{self.ORG_TITLE}")

    def build_boca_script(self) -> str:
        """ return fgl_script string """
        # self._order.get_ticket_fields()
        fgl_cmds = self._gen_fgl_script_from_ns()
        return ''.join(fgl_cmds)

    def _debug_boca_script_offsets(self) -> str:
        fgl_cmds = self._gen_fgl_script_from_ns()
        updated_fgl_cmds = []
        p = re.compile(r'<RC(\d+),(\d+)>(.*)')
        for cmd in fgl_cmds:
            m = p.search(cmd)
            if not m:
                updated_fgl_cmds.append(cmd)
            else:
                g = m.groups()
                updated_cmd = f'<RC{g[0]},{g[1]}>{g[0]},{g[1]}:{g[2]}'
                updated_fgl_cmds.append(updated_cmd)

        return ''.join(updated_fgl_cmds)


class CircusArtTicket(TaiwanAcrobaticTroupeTicket):
    """ FOCA """
    EVENTID = "859649002307"


class TaiwanPulseTicket(TaiwanAcrobaticTroupeTicket):
    """ Taiwan Pulse 2025 """
    EVENTID = "1292046719519"
