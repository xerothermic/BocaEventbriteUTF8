from typing import List
from attr import dataclass
from datetime import datetime

@dataclass
class Fields:
    """ Fields for printing """
    organization: str
    eventName: str
    eventLocation: str
    dateFrom: datetime
    dateTo: datetime
    price: str
    purchaser: str
    ticketType: str
    seatLocation: List[str]
    ticketId: int
    serialId: int

    @staticmethod
    def handle_long_string(roff, coff, string):
        """ Split long string intwo two when longer than 30 characters """
        roff2 = roff + 80
        tokens = string.split(' ')
        line1Tokens = ""
        line2Tokens = ""
        for token in tokens:
            if len(line1Tokens + token) < 30:
                line1Tokens += token + ' '
            else:
                line2Tokens += token + ' '

        return roff2 , f"<RC{roff},{coff}><TTF1,12>{line1Tokens}" + f"<RC{roff2},{coff}>{line2Tokens}"

    def __str__(self):
        roff = 0 # row offset
        coff = 65 # column offset
        strings = [f"<RC{roff},{coff}><TTF1,8>{self.organization}"]
        roff += 50
        roff, lines = Fields.handle_long_string(roff, coff, self.eventName)
        strings.append(lines)
        roff += 120
        strings.append(f"<RC{roff},{coff}><F3>{self.eventLocation}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.dateFrom.strftime('%c')} - {self.dateTo.strftime('%c')}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.price}")
        roff += 100
        strings.append(f"<RC{roff},{coff}><TTF1,8>{self.purchaser}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.ticketType}, {', '.join(self.seatLocation)}")

        # start again from the top row
        roff = 0
        coff = 1200
        strings.append(f"<RC{roff},{coff}><F3>#{self.ticketId}")
        coff += 300
        strings.append(f"<RC{roff},{coff}>#{self.ticketId}")
        roff += 50
        strings.append(f"<RC{roff},{coff}>{self.ticketType}")
        for token in self.seatLocation:
            roff += 50
            strings.append(f"<RC{roff},{coff}>{token}")
        roff += 50
        strings.append(f"<RC{roff},{coff}><QR5>"+"{"+str(self.serialId)+"}")
        roff += 250
        strings.append(f"<RC{roff},{coff}><F2>{self.serialId}")
        strings.append("<p>")
        return ''.join(strings)