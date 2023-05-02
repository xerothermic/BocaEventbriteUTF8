import logging
import click
from eventbrite_manager import EventbriteManager
from fields import BocaFields, build_boca_fields
from send_to_printer import send_to_printer
from util import peek

logger = logging.getLogger(__name__)

def configure_root_logger(logging_level=logging.INFO):
    """ Initialize root logger """
    root_logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(filename)s %(funcName)s:%(lineno)d - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    root_logger.setLevel(logging_level)

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    configure_root_logger(logging.DEBUG if debug else logging.INFO)

@cli.command() # @cli, not @click!
@click.option('--order_id', prompt='Enter your order id',
                help='Eventbrite Order ID.')
@click.option('--dry-run', is_flag=True, default=False, help='Dry run only, no printing.')
@click.option('--first-N', default=0, help='Print first N tickets only.')
@click.option('--ttf-font', default='TTF1', help='TTF font file on printer.', type=click.Choice(['TTF1', 'TTF2', 'TTF3']))
@click.option('--org-title', default='Taiwanese Association of Greater Seattle 西雅圖台灣同鄉會', help='Organization name.')
def eventbrite(order_id, dry_run, first_n, ttf_font, org_title):
    """ Print Eventbrite tickets """
    ebm = EventbriteManager()
    attendees = ebm.get_attendees_by_order_id(order_id)
    attendee1, attendees = peek(attendees)
    if attendee1 is None:
        logger.error(f"Order {order_id} does not exist.")
        return
    ev_detail = ebm.get_event_detail(attendee1.event_id)
    ev_detail.org_title = org_title
    for idx, p in enumerate(attendees):
        ticket_class_detail = ebm.get_ticket_class_detail(p.event_id, p.ticket_class_id)
        logger.debug(ticket_class_detail)
        p.ticket_description = ticket_class_detail.description
        bf = build_boca_fields(ev_detail, p, ttf_font)
        logger.debug(f"{idx=}:{bf}")
        if not dry_run and (first_n == 0 or idx < first_n):
            logger.info(f"Sending {idx} to printer")
            send_to_printer(bf)

if __name__ == '__main__':
    cli()
