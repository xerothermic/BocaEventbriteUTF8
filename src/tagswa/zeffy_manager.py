from datetime import datetime
import sys
from typing import Iterator
import logging
import os
import requests

from tagswa.abstraction.event import CommonEventFields
from tagswa.abstraction.zeffy import ZeffyAttendee

logger = logging.getLogger(__name__)

ZEFFY_API_BASE = 'https://api.zeffy.com/api/v1'


class ZeffyManager:
    """ Handle Zeffy API calls """

    def __init__(self):
        self._check_api_key()
        self._api_key = os.environ['ZEFFY_API_KEY']
        self._session = requests.Session()
        self._session.headers.update({
            'Authorization': f'Bearer {self._api_key}',
        })

    def _check_api_key(self):
        if 'ZEFFY_API_KEY' not in os.environ:
            logger.error("Please set the environment variable ZEFFY_API_KEY to your Zeffy API key")
            sys.exit(1)

    def _get(self, path: str, params: dict = None) -> dict:
        resp = self._session.get(f'{ZEFFY_API_BASE}{path}', params=params)
        resp.raise_for_status()
        return resp.json()

    def get_attendees_by_campaign_id(self, campaign_id: str) -> Iterator[ZeffyAttendee]:
        params = {'limit': 100, 'campaign': campaign_id, 'status': 'succeeded'}
        while True:
            data = self._get('/payments', params=params)
            for payment in data['data']:
                for item in payment['items']:
                    yield ZeffyAttendee.from_payment_api(payment, item)

            if not data.get('has_more'):
                break
            params['starting_after'] = data['next_cursor']

    def get_event_detail(self, campaign_id: str, occurrence_id: str = None) -> CommonEventFields:
        data = self._get(f'/campaigns/{campaign_id}')

        start_ts = data.get('start_date')
        end_ts = data.get('end_date')

        if occurrence_id and data.get('occurrences'):
            for occ in data['occurrences']:
                if occ['id'] == occurrence_id:
                    start_ts = occ.get('start') or occ.get('start_date') or start_ts
                    end_ts = occ.get('end') or occ.get('end_date') or end_ts
                    break

        return CommonEventFields(
            event_title=data['title'],
            event_start_datetime=datetime.fromtimestamp(start_ts) if start_ts else datetime.now(),
            event_end_datetime=datetime.fromtimestamp(end_ts) if end_ts else datetime.now(),
        )
