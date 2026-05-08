from datetime import datetime
from types import SimpleNamespace
from tagswa.boca_printer import BocaNullPrinter
from tagswa.abstraction.ticket import Ticket
from tagswa.abstraction.event import CommonEventFields
from tagswa.abstraction.eventbrite import EventbriteAttendee
from tagswa.abstraction.zeffy import ZeffyAttendee
from tagswa.meydenbauer_ticket import TaiwanAcrobaticTroupeTicket
from tagswa.scc_ticket import SCCTicket


def test_split_long_line1():
    """ contiguous long line without space """
    test_str = "01" * 20
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 1
    assert lines[0] == test_str


def test_split_short_line1():
    """ contiguous short line without space """
    test_str = "01" * 5
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 1
    assert lines[0] == test_str


def test_split_long_line2():
    """ long line with spaces """
    test_str = "01 " * 20
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 4
    assert lines[0] == ("01 " * 5).rstrip()
    assert lines[3] == ("01 " * 5).rstrip()


def test_split_short_line2():
    """ short line with spaces """
    test_str = "01 " * 4
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 1
    assert lines[0] == test_str


def test_split_long_short_line():
    """ long line without space + long line with spaces """
    test_str_long = "0" * 18
    test_str = test_str_long
    test_str += " "
    test_str += "01 " * 8
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 3
    assert lines[0] == test_str_long
    assert lines[1] == ("01 " * 5).rstrip()
    assert lines[2] != "01 " * 3  # trailing space is dropped in returned line
    assert lines[2] == ("01 " * 3).rstrip()


def test_split_ticket_class_name():
    test_str = 'TICKET CLASS NAME:'+'01 '*7
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 3
    assert lines[0] == 'TICKET CLASS'
    assert lines[1].startswith('NAME:')


def test_acrobatic_ticket_layout_null():
    """ Construct a dummy ticket with long fields """
    attendee = EventbriteAttendee(
        profile_name='PROFILE.NAME:' + '01' * 20,
        barcode='BARCODE:669179136910885398349001',
        price_display='PRICE: $30.00',
        order_id='6691791369',
        event_id='579945642027',
        ticket_class_id='12345',
        ticket_class_name='TICKET CLASS NAME:' + '01 ' * 7,
        assigned_unit_pairs=['01 ' * 2, '23 ' * 2, '34 ' * 2],
        ticket_description=None,
    )

    evf = CommonEventFields(
        event_title="EVENT TITLE:" + '23 ' * 22,
        event_start_datetime=datetime.now(),
        event_end_datetime=datetime.now())
    ticket = TaiwanAcrobaticTroupeTicket(attendee, evf)

    fgl_str = ticket.build_boca_script()
    print(fgl_str)
    printer = BocaNullPrinter()
    printer.print(fgl_str)


def test_eventbrite_attendee_from_attendee_api():
    """ Verify from_attendee_api correctly flattens nested SimpleNamespace """
    ns = SimpleNamespace()
    ns.profile = SimpleNamespace(name='John Doe')
    ns.barcodes = [SimpleNamespace(barcode='123456789')]
    ns.costs = SimpleNamespace(gross=SimpleNamespace(display='$25.00'))
    ns.order_id = '99999'
    ns.event_id = '11111'
    ns.ticket_class_id = '22222'
    ns.ticket_class_name = 'General Admission'
    ns.assigned_unit = SimpleNamespace(pairs=[['Section', 'A'], ['Row', '1']])

    attendee = EventbriteAttendee.from_attendee_api(ns)
    assert attendee.profile_name == 'John Doe'
    assert attendee.barcode == '123456789'
    assert attendee.price_display == '$25.00'
    assert attendee.order_id == '99999'
    assert attendee.event_id == '11111'
    assert attendee.ticket_class_name == 'General Admission'
    assert attendee.assigned_unit_pairs == [['Section', 'A'], ['Row', '1']]
    assert attendee.ticket_description is None


def test_zeffy_attendee_from_payment_api():
    """ Verify from_payment_api maps Zeffy API dict structure """
    payment = {
        'id': 'pay-uuid-123',
        'campaign_id': 'camp-uuid-456',
        'occurrence_id': 'occ-uuid-789',
        'buyer': {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
        },
    }
    item = {
        'id': 'ticket-uuid-abc',
        'amount': 2000,
        'rate_id': 'rate-uuid-def',
    }

    attendee = ZeffyAttendee.from_payment_api(payment, item)
    assert attendee.ticket_id == 'ticket-uuid-abc'
    assert attendee.profile_name == 'Jane Smith'
    assert attendee.amount_display == '$20.00'
    assert attendee.payment_id == 'pay-uuid-123'
    assert attendee.campaign_id == 'camp-uuid-456'
    assert attendee.occurrence_id == 'occ-uuid-789'
    assert attendee.rate_id == 'rate-uuid-def'
    assert attendee.buyer_email == 'jane@example.com'


def test_zeffy_attendee_null_name_becomes_dear_guest():
    """ Verify None first/last name falls back to 'Dear Guest' """
    payment = {
        'id': 'pay-uuid-123',
        'campaign_id': 'camp-uuid-456',
        'occurrence_id': 'occ-uuid-789',
        'buyer': {
            'first_name': None,
            'last_name': None,
            'email': None,
        },
    }
    item = {
        'id': 'ticket-uuid-abc',
        'amount': 0,
        'rate_id': 'rate-uuid-def',
    }

    attendee = ZeffyAttendee.from_payment_api(payment, item)
    assert attendee.profile_name == 'Dear Guest'
    assert attendee.buyer_email == ''


def test_scc_ticket_qr_url():
    """ Verify SCC ticket FGL contains QRV7+QR6 with Zeffy URL """
    attendee = ZeffyAttendee(
        ticket_id='bf4491cf-cbe9-4b65-9246-8ec4588f8f5a',
        profile_name='Test User',
        amount_display='$20.00',
        payment_id='pay-123',
        campaign_id='52563cbe-97d0-4fd6-a708-347f0f674a86',
        occurrence_id='occ-123',
        rate_id='rate-123',
        buyer_email='test@example.com',
    )
    evf = CommonEventFields(
        event_title='TAHW 2026',
        event_start_datetime=datetime.now(),
        event_end_datetime=datetime.now(),
    )
    ticket = SCCTicket(attendee, evf)
    fgl_str = ticket.build_boca_script()

    assert '<QRV7><QR6>' in fgl_str
    assert 'https://www.zeffy.com/ticket/bf4491cf-cbe9-4b65-9246-8ec4588f8f5a' in fgl_str
    assert 'Test User' in fgl_str
    assert '$20.00' in fgl_str
    assert '<p>' in fgl_str
