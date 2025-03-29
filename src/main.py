import itertools
import logging
import click

from tagswa.woman_ticket import WomanTicket
from tagswa.meydenbauer_ticket import TaiwanAcrobaticTroupeTicket, CircusArtTicket, TaiwanPulseTicket
from tagswa.summer_picnic_ticket import SummerPicnic2023Ticket
from tagswa.eventbrite_manager import EventbriteManager
from tagswa.boca_printer import BocaTcpPrinter, BocaNullPrinter

logger = logging.getLogger(__name__)


def configure_root_logger(logging_level=logging.INFO):
    """ Initialize root logger """
    root_logger = logging.getLogger()
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging_level)


def peek(it):
    """ Peek the first element and return the original iterator """
    try:
        first = next(it)
    except StopIteration:
        return None, None
    return first, itertools.chain([first], it)


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    configure_root_logger(logging.DEBUG if debug else logging.INFO)


@cli.command()  # @cli, not @click!
@click.option('--order_id', prompt='Enter your order id',
              help='Eventbrite Order ID.')
@click.option("--include-used", is_flag=True, default=False, help="Include attendees even if the tickets have been used")
@click.option('--dry-run', is_flag=True, default=False, help='Dry run only, no printing.')
@click.option('--first-N', default=0, help='Print first N tickets only.')
@click.option("--skip-N", default=0, help="Skip first N tickets before printing.")
@click.option('--ttf-font', default='TTF1', help='TTF font file on printer.', type=click.Choice(['TTF1', 'TTF2', 'TTF3']))
def eventbrite(order_id, include_used, dry_run, first_n, skip_n, ttf_font):
    """ Print Eventbrite tickets """
    ebm = EventbriteManager()
    attendees = ebm.get_attendees_by_order_id(
        order_id, unused_only=not include_used)
    attendee1, attendees = peek(attendees)
    if attendee1 is None:
        logger.error(f"Order {order_id} does not exist.")
        return
    common_event_fields = ebm.get_event_detail(attendee1.event_id)
    printer = _setup_boca_printer(dry_run)

    if first_n:
        logger.info(f"{first_n=}")
        attendees = [next(attendees) for _ in range(first_n)]
        attendees = iter(attendees)
    if skip_n:
        logger.info(f"{skip_n=}")
        [next(attendees) for _ in range(skip_n)]

    for idx, p in enumerate(attendees):
        ticket_class_detail = ebm.get_ticket_class_detail(
            p.event_id, p.ticket_class_id)
        logger.debug(ticket_class_detail)
        p.ticket_description = ticket_class_detail.description
        if p.event_id == TaiwanAcrobaticTroupeTicket.EVENTID:
            ticket = TaiwanAcrobaticTroupeTicket(
                p, common_event_fields, ttf_font)
        elif p.event_id == CircusArtTicket.EVENTID:
            ticket = CircusArtTicket(p, common_event_fields, ttf_font)
        elif p.event_id == TaiwanPulseTicket.EVENTID:
            ticket = TaiwanPulseTicket(p, common_event_fields, ttf_font)
        elif p.event_id == SummerPicnic2023Ticket.EVENTID:
            if int(p.barcodes[0].barcode) >= 733198138911988989009001:
                ticket = SummerPicnic2023Ticket(
                    p, common_event_fields, ttf_font)
            else:
                continue
        elif p.event_id == WomanTicket.EVENTID:
            ticket = WomanTicket(p, common_event_fields, ttf_font)
        else:
            raise ValueError(
                f"Don't know how to create ticket for {p.event_id=}")
        # logger.debug(f"{idx=}:{bf}")
        # if first_n == 0 or idx < first_n:
        logger.info(f"Sending {idx} to printer")
        printer.print(ticket.build_boca_script())


def _setup_boca_printer(dry_run):
    if dry_run:
        printer = BocaNullPrinter()
    else:
        printer = BocaTcpPrinter()
    return printer


if __name__ == '__main__':
    cli()
