from eventbrite import Eventbrite
import os

EVENT_ID = '579945642027'
eb = Eventbrite(os.environ.get('EVENTBRITE_TOKEN'))

def get_attendees():
    resp = eb.get(f'/events/{EVENT_ID}/attendees/', {'expand': 'assigned_unit'})
    # TODO: Handle pagination
    pagination, attendees = resp['pagination'], resp['attendees']

    return attendees

def get_event_text():
    return eb.get_event(EVENT_ID)['name']['text']

def get_venue_text():
    return eb.get(f"/events/{EVENT_ID}", data={"expand":"venue"})['venue']['address']['localized_address_display']

def get_event_start_time():
    return eb.get(f"/events/{EVENT_ID}")['start']['local']

def get_event_end_time():
    return eb.get(f"/events/{EVENT_ID}")['end']['local']
    

if __name__ == "__main__":
    attendees = get_attendees()
    for attendee in attendees:
        print(attendee['profile']['name'], attendee['id'], attendee['order_id'], attendee['barcodes'], attendee['assigned_unit']['pairs'])