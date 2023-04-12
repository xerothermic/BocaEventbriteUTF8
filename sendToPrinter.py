import socket
from datetime import datetime
from fields import Fields


IP = '192.168.55.186'
PORT = 9100

def send_to_printer(fields: Fields):
    """ Send fields to Boca printer """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((IP, PORT))
        print('Connected to printer')
        sent = s.sendall(f'{fields}'.encode())
        print(f'Printed {fields=}')

if __name__ == '__main__':
    f = Fields(
        organization='Taiwanese Association of Greater Seattle 西雅圖台灣同鄉會',
        eventName='Taiwan Reminiscence by Taiwan Acrobatic Troup 【台灣追想曲】台灣特技團',
        eventLocation='Meydenbauer Center, 11100 Northeast 6th Street, Belleveue, WA 98004',
        dateFrom=datetime.strptime('2023-05-19 19:00:00', '%Y-%m-%d %H:%M:%S'),
        dateTo=datetime.strptime('2023-05-19 21:00:00', '%Y-%m-%d %H:%M:%S'),
        price='$30.00',
        purchaser='Bear Chen',
        ticketType='Standard Adults',
        seatLocation=['Section: C', 'Row: G', 'Seat: 107'],
        ticketId=6371643849,
        serialId=637164384910378220589001
    )

    print("Sending:",f," to printer ", IP, ":", PORT)
    send_to_printer(f)