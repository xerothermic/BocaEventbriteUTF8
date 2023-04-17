import socket
from datetime import datetime
from fields import BocaFields, build_boca_fields

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

# IP = '192.168.55.186'
IP = '10.0.0.192'
PORT = 9100

def download_ttf_font():
    """ Download TTF font from Boca printer """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        # s.settimeout(1.5) # cannot set this too short, it will cause send to time out too.
        logger.info('Connected to printer')
        s.sendall('<S7>'.encode())
        try:
            resp = s.recv(1024)
        except socket.timeout:
            pass
        finally:
            logger.info(f'<S7> resp: {resp}')

        with open('./fonts/TaigiGenSekiGothic/TaigiGenSekiG-TL-H.ttf', 'rb') as f:
            ttf = f.read()
            logger.info('Loaded TTF font')
            sent = s.sendall(f'<ID2><ttf{len(ttf)}>'.encode()+ttf)

        s.sendall('<S7>'.encode())
        try:
            resp = s.recv(1024)
        except socket.timeout:
            pass
        finally:
            logger.info(f'<S7> resp: {resp}')


def send_to_printer(fields: BocaFields):
    """ Send fields to Boca printer """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        print('Connected to printer')
        sent = s.sendall(f'{fields}'.encode())
        print(f'Printed {fields=}')

if __name__ == '__main__':
    event_detail = {'name': {'text': 'Taiwan Reminiscence by Taiwan Acrobatic Troup 【台灣追想曲】台灣特技團'}}
    event_detail['venue'] = {'name': 'Meydenbauer Center', 'address': {'localized_address_display': '11100 Northeast 6th Street, Belleveue, WA 98004'}}
    event_detail['start'] = {'local': '2023-05-19T19:00:00'}
    event_detail['end'] = {'local': '2023-05-19T21:00:00'}
    attendee = {'profile': {'name': 'Bear Chen'},
        'costs': {'gross': {'display': '$30.00'}},
        'ticket_class_name': 'Standard Adults',
        'assigned_unit': {'pairs': [['Section', 'C'], ['Row', 'G'], ['Seat', '107']]},
        'order_id': 6371643849,
        'barcodes': [{'barcode': 637164384910378220589001}]}
    bf = build_boca_fields(gen_obj(event_detail), gen_obj(attendee))
    
    print("Sending:", bf," to printer ", IP, ":", PORT)
    send_to_printer(bf)