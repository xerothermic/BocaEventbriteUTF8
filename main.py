import click
from eventbrite_manager import EventbriteManager
from fields import BocaFields, build_boca_fields
from send_to_printer import send_to_printer
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@click.command()
@click.option('--event_id', default=579945642027, help='Eventbrite Event ID for 傳統週.')
@click.option('--order_id', prompt='Enter your order id',
                help='Eventbrite Order ID.')
@click.option('--dry-run', default=False, help='Dry run only, no printing.')
@click.option('--first-N', default=0, help='Print first N tickets only.')
@click.option('--ttf-font', default='TTF1', help='TTF font file on printer.', type=click.Choice(['TTF1', 'TTF2', 'TTF3']))
def main(event_id, order_id, dry_run, first_n, ttf_font):
    ebm = EventbriteManager()
    attendees = ebm.get_attendees_by_order_id(order_id)
    ev_detail = ebm.get_event_detail(event_id)
    for idx, p in enumerate(attendees):
        bf = build_boca_fields(ev_detail, p, ttf_font)
        click.echo(f"{idx=}:{bf}")
        if not dry_run and (first_n == 0 or idx < first_n):
            logger.debug("Sending to printer")
            send_to_printer(bf)

if __name__ == '__main__':
    main()