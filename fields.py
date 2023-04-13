from typing import List
from attr import dataclass
from datetime import datetime

@dataclass
class BocaSettings:
    ttf_font: str = 'TTF1'
    # ttf_font_size: int = 12

@dataclass
class BocaFields:
    """ Fields for printing """
    org_title: str
    event_title: str
    venue_title: str
    venue_addr: str
    event_start_time: datetime
    event_end_time: datetime
    price: str
    attendee: str
    ticket_type: str
    seat_detail: List[str]
    ticket_id: int
    barcode: int
    # BocaSettings
    boca_settings: BocaSettings = BocaSettings()

    def _break_long_line(self, roff, coff, string):
        """ Break long string into two when len(string) > 30 characters """
        roff2 = roff + 60
        tokens = string.split(' ')
        first_line_tokens = ""
        second_line_tokens = ""
        for token in tokens:
            if len(first_line_tokens + token) < 30:
                first_line_tokens += token + ' '
            else:
                second_line_tokens += token + ' '

        ttf = self.boca_settings.ttf_font
        return roff2 , f"<RC{roff},{coff}><{ttf},12>{first_line_tokens}" + f"<RC{roff2},{coff}>{second_line_tokens}"

    def __str__(self):
        roff = 0 # row offset
        coff = 65 # column offset
        ttf = self.boca_settings.ttf_font
        strings = [f"<RC{roff},{coff}><{ttf},8>{self.org_title}"]
        roff += 50
        roff, lines = self._break_long_line(roff, coff, self.event_title)
        strings.append(lines)
        roff += 100
        strings.append(f"<RC{roff},{coff}><F3>{self.venue_title}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.venue_addr}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.event_start_time.strftime('%c')} - {self.event_end_time.strftime('%c')}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.price}")
        roff += 75
        strings.append(f"<RC{roff},{coff}><{ttf},8>{self.attendee}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.ticket_type}, {', '.join(self.seat_detail)}")

        # start again from the top row
        roff = 0
        coff = 1200
        strings.append(f"<RC{roff},{coff}><F3>#{self.ticket_id}")
        coff += 300
        strings.append(f"<RC{roff},{coff}>#{self.ticket_id}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.ticket_type}")
        for token in self.seat_detail:
            roff += 50
            strings.append(f"<RC{roff},{coff}>{token}")
        roff += 50
        strings.append(f"<RC{roff},{coff}><QR5>"+"{"+str(self.barcode)+"}")
        roff += 250
        strings.append(f"<RC{roff},{coff}><F2>{self.barcode}")
        strings.append("<p>")
        return ''.join(strings)

def build_boca_fields(ev_detail, attendee, ttf_font='TTF1'):
    return BocaFields(
        org_title='Taiwanese Association of Greater Seattle 西雅圖台灣同鄉會',
        event_title=ev_detail.name.text,
        venue_title=ev_detail.venue.name,
        venue_addr=ev_detail.venue.address.localized_address_display,
        event_start_time=datetime.strptime(ev_detail.start.local, '%Y-%m-%dT%H:%M:%S'),
        event_end_time=datetime.strptime(ev_detail.end.local, '%Y-%m-%dT%H:%M:%S'),
        price=attendee.costs.base_price.display,
        attendee=attendee.profile.name,
        ticket_type=attendee.ticket_class_name,
        seat_detail=[': '.join(pair) for pair in attendee.assigned_unit.pairs],
        ticket_id=attendee.order_id,
        barcode=attendee.barcodes[0].barcode,
        boca_settings=BocaSettings(ttf_font=ttf_font),
    )
