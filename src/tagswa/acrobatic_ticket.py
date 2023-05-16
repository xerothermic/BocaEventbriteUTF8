from typing import List
from attr import dataclass
from tagswa.eventbrite_manager import EventbriteManager
from tagswa.abstraction.eventbrite import CommonEventFields
from types import SimpleNamespace
from tagswa.abstraction.ticket import Ticket

class TaiwanAcrobaticTroupeTicket(Ticket):
    EVENTID = "579945642027"

    """ Represent Taiwan Reminiscence by Taiwan Acrobatic Troupe event ticket """
    def __init__(self, ns: SimpleNamespace, CommonEventFields: CommonEventFields):
        if self._missing_required_fields(ns):
            raise ValueError("missing fields")
        self._ns = ns
        self._ev_details = CommonEventFields
        
    @staticmethod
    def _missing_required_fields(ns: SimpleNamespace):
        return False
    
    def _gen_fgl_script_from_ns(self):
        ns = self._ns
        evd = self._ev_details
        roff = 0 # row offset
        coff = 65 # column offset
        ttf = 'TTF1' # self.boca_settings.ttf_font
        strings = [f"<RC{roff},{coff}><{ttf},8>{evd.org_title}"]
        roff += 50

        strings.append(f"<TTF1,12>")
        titles = Ticket.split_long_line(evd.event_title, 30)
        for line_id, title_fragment in enumerate(titles):
            strings.append(f"<RC{roff},{coff}>{title_fragment}")
            roff += 60

            if line_id >= 2:
                raise ValueError("Event title longer than two lines may mess up layout.")

        roff += 40
        strings.append(f"<RC{roff},{coff}><F3>{evd.venue_title}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{evd.venue_addr}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{evd.event_start_datetime.strftime('%c')} - {evd.event_end_datetime.strftime('%c')}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{ns.costs.gross.display}")
        roff += 75
        strings.append(f"<RC{roff},{coff}><{ttf},8>{ns.profile.name}")
        roff += 50
        seat_detail=[': '.join(pair) for pair in ns.assigned_unit.pairs]
        strings.append(f"<RC{roff},{coff}>{ns.ticket_class_name}{', ' if seat_detail else ''}{', '.join(seat_detail)}")

        if ns.ticket_description:
            coff = 235
            roff = 390
            strings.append(f"<RC{roff},{coff}><{ttf},8>{ns.ticket_description}")

        # start again from the top row
        roff = 0
        coff = 1200
        strings.append(f"<RC{roff},{coff}><F3>#{ns.order_id}")
        coff += 300
        strings.append(f"<RC{roff},{coff}>#{ns.order_id}")
        roff += 10

        for l in Ticket.split_long_line(ns.ticket_class_name, char_per_line=16):
            roff += 30
            strings.append(f"<RC{roff},{coff}>{l}")

        for token in seat_detail:
            roff += 35
            strings.append(f"<RC{roff},{coff}>{token}")
        roff += 50
        strings.append(f"<RC{roff},{coff}><QR5>"+"{"+str(ns.barcodes[0].barcode)+"}")
        roff += 250
        strings.append(f"<RC{roff},{coff}><F2>{ns.barcodes[0].barcode}")
        strings.append("<p>")
        return ''.join(strings)

    def build_boca_script(self) -> str:
        """ return fgl_script string """
        # self._order.get_ticket_fields()
        return self._gen_fgl_script_from_ns()