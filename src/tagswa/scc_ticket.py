import re
import logging
from typing import List

from tagswa.abstraction.ticket import Ticket
from tagswa.abstraction.event import CommonEventFields
from tagswa.abstraction.zeffy import ZeffyAttendee

logger = logging.getLogger(__name__)

ZEFFY_TICKET_URL = 'https://www.zeffy.com/ticket'


class SCCTicket(Ticket):
    """ Shoreline Community College venue ticket (Taiwanese American Heritage Week) """
    EVENTID = "52563cbe-97d0-4fd6-a708-347f0f674a86"
    ORG_TITLE = "Taiwanese Association of Greater Seattle 大西雅圖台灣同鄉會"
    VENUE_TITLE = "Shoreline Community College Main Auditorium"
    VENUE_ADDR = "16101 Greenwood Ave N, Shoreline, WA 98133"

    def __init__(self, attendee: ZeffyAttendee, evf: CommonEventFields, ttf_font: str = "TTF1"):
        self._attendee = attendee
        self._ev_details = evf
        self._ttf_font = ttf_font

    def _gen_fgl_script_from_ns(self) -> List[str]:
        strings = []
        self._place_org_title(strings)
        self._place_event_title(strings)
        self._place_venue_info(strings)
        self._place_event_time(strings)
        self._place_price(strings)
        self._place_attendee_name(strings)
        self._place_order_id(strings)
        self._place_barcode(strings)
        self._place_cut_cmd(strings)
        return strings

    def _place_cut_cmd(self, strings):
        strings.append("<p>")

    def _place_barcode(self, strings):
        url = f"{ZEFFY_TICKET_URL}/{self._attendee.ticket_id}"
        strings.append(f"<RC125,1525><QRV7><QR6>{{{url}}}")
        strings.append(f"<RC510,1500><F2>P:{self._attendee.payment_id}")
        strings.append(f"<RC540,1500><F2>T:{self._attendee.ticket_id}")

    def _place_order_id(self, strings):
        strings.append("<F3>")
        strings.append(f"<RC0,1200>#{self._attendee.payment_id[:8]}")
        strings.append(f"<RC0,1500>#{self._attendee.payment_id[:8]}")

    def _place_attendee_name(self, strings):
        strings.append(
            f"<RC470,65><{self._ttf_font},8>{self._attendee.profile_name}")

    def _place_price(self, strings):
        strings.append(f"<RC395,65>{self._attendee.amount_display}")

    def _place_event_time(self, strings):
        strings.append("<RC345,65>{0} - {1}".format(
            self._ev_details.event_start_datetime.strftime('%c'),
            self._ev_details.event_end_datetime.strftime('%c')))

    def _place_venue_info(self, strings):
        strings.append("<F3>")
        strings.append(f"<RC245,65>{self.VENUE_TITLE}")
        strings.append(f"<RC295,65>{self.VENUE_ADDR}")

    def _place_event_title(self, strings):
        roff = 100
        strings.append(f"<{self._ttf_font},10>")
        titles = Ticket.split_long_line(self._ev_details.event_title, 52)
        if len(titles) > 3:
            raise ValueError("Event title exceed three lines.")
        for title_fragment in titles:
            strings.append(f"<RC{roff},65>{title_fragment}")
            roff += 50

    def _place_org_title(self, strings):
        strings.append(
            f"<RC30,65><{self._ttf_font},8>{self.ORG_TITLE}")

    def build_boca_script(self) -> str:
        """ return fgl_script string """
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
