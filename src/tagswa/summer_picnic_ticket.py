import re
import logging

logger = logging.getLogger(__name__)

from tagswa.abstraction.event import CommonEventFields
from tagswa.abstraction.eventbrite import EventbriteAttendee
from tagswa.abstraction.ticket import Ticket

class SummerPicnic2023Ticket(Ticket):
    """ Summer picnic event """
    EVENTID = "675702834367"
    ORG_TITLE = "TAGS"
    VENUE_TITLE = "Marymoor Park"
    VENUE_ADDR = "Redmond, WA"

    def __init__(self, attendee: EventbriteAttendee, evf: CommonEventFields, ttf_font: str = "TTF1"):
        self._attendee = attendee
        self._ev_details = evf
        self._ttf_font = ttf_font

    def _gen_fgl_script_from_ns(self):
        strings = []
        logger.debug("_place_org_title")
        self._place_org_title(strings)
        self._place_event_title(strings)
        self._place_venue_info(strings)
        self._place_event_time(strings)
        self._place_price(strings)
        self._place_attendee_name(strings)
        self._place_ticket_description(strings)
        self._place_order_id(strings)
        self._place_ticket_class(strings)
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
        strings.append("<RC200,1550><QR5>"+"{"+self._attendee.barcode+"}")
        strings.append(f"<RC440,1550><F2>{self._attendee.barcode}")

    def _place_ticket_class(self, strings):
        roff = 10
        strings.append(f"<{self._ttf_font},8>")

        for l in Ticket.split_long_line(self._attendee.ticket_class_name, char_per_line=16):
            roff += 30
            strings.append(f"<RC{roff},1500>{l}")

    def _place_order_id(self, strings):
        # start again from the top row
        strings.append("<F3>")
        strings.append(f"<RC0,1200>#{self._attendee.order_id}")
        strings.append("<F3>")
        strings.append(f"<RC0,1500>#{self._attendee.order_id}")

    def _place_ticket_description(self, strings):
        if not self._attendee.ticket_description:
            return

        strings.append(f"<RC390,235><{self._ttf_font},8>{self._attendee.ticket_description}")

    def _place_attendee_name(self, strings):
        strings.append(f"<RC480,65><{self._ttf_font},8>{self._attendee.profile_name}")

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
        strings.append(f"<RC0,65><{self._ttf_font},9>{self.ORG_TITLE}")

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