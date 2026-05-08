from dataclasses import dataclass

@dataclass
class ZeffyAttendee:
    """ Zeffy attendee data extracted from the payments API """
    ticket_id: str         # items[].id — UUID used in QR URL
    profile_name: str      # buyer.first_name + " " + buyer.last_name
    amount_display: str    # formatted from items[].amount (cents to dollars)
    payment_id: str        # payment.id
    campaign_id: str       # campaign_id — maps to EVENTID for dispatch
    occurrence_id: str     # occurrence_id — matches occurrence for start/end time
    rate_id: str           # items[].rate_id — ticket type
    buyer_email: str       # buyer.email

    @classmethod
    def from_payment_api(cls, payment: dict, item: dict) -> "ZeffyAttendee":
        """ Create ZeffyAttendee from raw Zeffy payment API response """
        buyer = payment['buyer']
        amount_cents = item['amount']
        return cls(
            ticket_id=item['id'],
            profile_name=f"{buyer.get('first_name') or ''} {buyer.get('last_name') or ''}".strip() or 'Dear Guest',
            amount_display=f"${amount_cents / 100:.2f}",
            payment_id=payment['id'],
            campaign_id=payment['campaign_id'],
            occurrence_id=payment.get('occurrence_id', ''),
            rate_id=item['rate_id'],
            buyer_email=buyer.get('email') or '',
        )
