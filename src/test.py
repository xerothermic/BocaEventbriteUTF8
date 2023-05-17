from datetime import datetime
from types import SimpleNamespace
from tagswa.abstraction.ticket import Ticket
from tagswa.abstraction.eventbrite import CommonEventFields
from tagswa.boca_printer import BocaTcpPrinter, BocaNullPrinter
from tagswa.acrobatic_ticket import TaiwanAcrobaticTroupeTicket

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
    assert lines[2] != "01 " * 3 # trailing space is dropped in returned line
    assert lines[2] == ("01 " * 3).rstrip()

def test_split_ticket_class_name():
    test_str = 'TICKET CLASS NAME:'+'01 '*7
    lines = Ticket.split_long_line(test_str, 16)
    assert len(lines) == 3
    assert lines[0] == 'TICKET CLASS'
    assert lines[1].startswith('NAME:')

def test_acrobatic_ticket_layout_null():
    """ Construct a dummy ticket with long"""
    ns = SimpleNamespace()
    ns.barcodes = [SimpleNamespace()]
    ns.barcodes[0].barcode = 'BARCODE:669179136910885398349001'
    ns.assigned_unit = SimpleNamespace()
    ns.assigned_unit.pairs = ['01 '*2,'23 '*2,'34 '*2]
    ns.ticket_class_name = 'TICKET CLASS NAME:'+'01 '*7
    ns.order_id = '6691791369'
    ns.ticket_description = None
    ns.profile = SimpleNamespace()
    ns.profile.name = 'PROFILE.NAME:' + '01' * 20
    ns.costs = SimpleNamespace()
    ns.costs.gross = SimpleNamespace()
    ns.costs.gross.display = 'PRICE: $30.00'

    evf = CommonEventFields(
        org_title="ORG TITLE:" + '01' * 20,
        event_title="EVENT TITLE:" + '23 ' * 22,
        venue_title="VENUE TITLE:" + '45' * 20,
        venue_addr="VENUE ADDR:" + '67' * 20,
        event_start_datetime=datetime.now(),
        event_end_datetime=datetime.now())
    ticket = TaiwanAcrobaticTroupeTicket(ns, evf)

    fgl_str = ticket.build_boca_script()
    print(fgl_str)
    # printer = BocaTcpPrinter()
    printer = BocaNullPrinter()
    printer.print(fgl_str)
