import itertools
import logging
import click

from tagswa.woman_ticket import WomanTicket
from tagswa.meydenbauer_ticket import TaiwanAcrobaticTroupeTicket, CircusArtTicket, TaiwanPulseTicket
from tagswa.summer_picnic_ticket import SummerPicnic2023Ticket
from tagswa.scc_ticket import SCCTicket
from tagswa.eventbrite_manager import EventbriteManager
from tagswa.zeffy_manager import ZeffyManager
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


def common_options(f):
    """ Shared CLI options for all ticket printing commands """
    f = click.option('--dry-run', is_flag=True, default=False, help='Dry run only, no printing.')(f)
    f = click.option('--first-N', default=0, help='Print first N tickets only.')(f)
    f = click.option("--skip-N", default=0, help="Skip first N tickets before printing.")(f)
    f = click.option('--ttf-font', default='TTF1', help='TTF font file on printer.', type=click.Choice(['TTF1', 'TTF2', 'TTF3']))(f)
    return f


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    configure_root_logger(logging.DEBUG if debug else logging.INFO)


@cli.command()  # @cli, not @click!
@click.option('--order_id', prompt='Enter your order id',
              help='Eventbrite Order ID.')
@click.option("--include-used", is_flag=True, default=False, help="Include attendees even if the tickets have been used")
@common_options
def eventbrite(order_id, include_used, dry_run, first_n, skip_n, ttf_font):
    """ Print Eventbrite tickets """
    ebm = EventbriteManager()
    attendees = ebm.get_attendees_by_order_id(
        order_id, unused_only=not include_used)
    attendee1, attendees = peek(attendees)
    if attendee1 is None:
        logger.error(f"Order {order_id} does not exist.")
        return
    event_detail = ebm.get_event_detail(attendee1.event_id)
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
                p, event_detail, ttf_font)
        elif p.event_id == CircusArtTicket.EVENTID:
            ticket = CircusArtTicket(p, event_detail, ttf_font)
        elif p.event_id == TaiwanPulseTicket.EVENTID:
            ticket = TaiwanPulseTicket(p, event_detail, ttf_font)
        elif p.event_id == SummerPicnic2023Ticket.EVENTID:
            if int(p.barcode) >= 733198138911988989009001:
                ticket = SummerPicnic2023Ticket(
                    p, event_detail, ttf_font)
            else:
                continue
        elif p.event_id == WomanTicket.EVENTID:
            ticket = WomanTicket(p, event_detail, ttf_font)
        else:
            raise ValueError(
                f"Don't know how to create ticket for {p.event_id=}")
        # logger.debug(f"{idx=}:{bf}")
        # if first_n == 0 or idx < first_n:
        logger.info(f"Sending {idx} to printer")
        printer.print(ticket.build_boca_script())


ZEFFY_TICKET_CLASSES = [SCCTicket]
ZEFFY_CAMPAIGN_MAP = {cls.EVENTID: cls for cls in ZEFFY_TICKET_CLASSES}


@cli.command()
@click.option('--payment-id', default=None, help='Filter by Zeffy Payment ID.')
@click.option('--ticket-id', default=None, help='Filter by Zeffy Ticket ID.')
@click.option('--search', default=None, help='Search by name or email (case-insensitive partial match).')
@common_options
def zeffy(payment_id, ticket_id, search, dry_run, first_n, skip_n, ttf_font):
    """ Print Zeffy tickets """
    if not payment_id and not ticket_id and not search:
        raise click.UsageError("Provide at least one of --payment-id, --ticket-id, or --search.")

    zm = ZeffyManager()

    # Fetch attendees from all registered Zeffy campaigns
    all_attendees = []
    for campaign_id in ZEFFY_CAMPAIGN_MAP:
        all_attendees.extend(zm.get_attendees_by_campaign_id(campaign_id))

    # Filter
    if payment_id:
        matches = [a for a in all_attendees if a.payment_id == payment_id]
    elif ticket_id:
        matches = [a for a in all_attendees if a.ticket_id == ticket_id]
    else:
        q = search.lower()
        matches = [a for a in all_attendees
                   if q in a.profile_name.lower() or q in (a.buyer_email or '').lower()]

    if not matches:
        logger.error("No matching attendees found.")
        return

    logger.info(f"Found {len(matches)} matching attendee(s)")

    # Cache event details per campaign
    event_details = {}
    printer = _setup_boca_printer(dry_run)

    if first_n:
        matches = matches[:first_n]
    if skip_n:
        matches = matches[skip_n:]

    for idx, p in enumerate(matches):
        if p.campaign_id not in event_details:
            event_details[p.campaign_id] = zm.get_event_detail(p.campaign_id, p.occurrence_id)

        ticket_cls = ZEFFY_CAMPAIGN_MAP.get(p.campaign_id)
        if not ticket_cls:
            raise ValueError(f"Unknown campaign {p.campaign_id}")

        ticket = ticket_cls(p, event_details[p.campaign_id], ttf_font)
        logger.info(f"Sending {idx}: {p.profile_name} to printer")
        printer.print(ticket.build_boca_script())


def _setup_boca_printer(dry_run):
    if dry_run:
        printer = BocaNullPrinter()
    else:
        printer = BocaTcpPrinter()
    return printer


if __name__ == '__main__':
    cli()
