from datetime import datetime
from eventbriteConnector import get_attendees, get_event_text, get_venue_text, get_event_start_time, get_event_end_time
from sendToPrinter import send_to_printer
from fields import Fields

def main():
    attendees = get_attendees()
    f = Fields(
        organization='Taiwanese Association of Greater Seattle 西雅圖台灣同鄉會',
        eventName=get_event_text(),
        eventLocation=get_venue_text(),
        dateFrom=datetime.strptime(get_event_start_time(), '%Y-%m-%dT%H:%M:%S'),
        dateTo=datetime.strptime(get_event_end_time(), '%Y-%m-%dT%H:%M:%S'),
        price=None,
        purchaser=None,
        ticketType=None,
        seatLocation=None,
        ticketId=None,
        serialId=None        
    )
    for idx, attendee in enumerate(attendees):
        f.price = attendee['costs']['base_price']['display']
        f.purchaser = attendee['profile']['name']
        f.ticketType = attendee['ticket_class_name'] #TODO: how to find Standard Adult?
        f.seatLocation = [': '.join(pair) for pair in attendee['assigned_unit']['pairs']]
        f.ticketId = attendee['order_id']
        f.serialId = attendee['barcodes'][0]['barcode']
        print(f)

        if idx == 4 or idx == len(attendees) - 2:
            send_to_printer(f)

if __name__ == "__main__":
    main()
