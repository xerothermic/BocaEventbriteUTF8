import logging
import socket
from tagswa.abstraction.ticket import Ticket
from tagswa.abstraction.boca import Boca

logger = logging.getLogger(__name__)

class BocaTcpRespError(Exception):
    """ Represent Boca printer tcp response error """
    pass

class BocaNullPrinter(Boca):
    """ For simulation """
    def print(self, fgl_script: str):
        logger.info(f"Received:{fgl_script}")

class BocaTcpPrinter(Boca):
    """ Implemented a Boca printer via TCP interface """
    def __init__(self, ip='10.0.0.192', port=9100):
        self._sock = self._open_socket(ip, port)

    def _open_socket(self, ip: str, port: int):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        logger.info(f'Connected to Boca printer. Addr={ip}:{port}')
        return sock

    def print(self, fgl_script: str):
        self._sock.sendall(fgl_script.encode())
        logger.info(f'Printed {fgl_script}')

    def download_logo(self, logo_file_path: str):
        """ download 1-bit bmp logo to Boca printer """
        with open(logo_file_path, 'rb') as fp:
            logo = fp.read()
            logger.info(f'{logo_file_path=} contain {len(logo)} bytes.')
            print(f'{logo_file_path=} contain {len(logo)} bytes.')

            esc = chr(27).encode()
            self._sock.sendall(esc + f'<bmp><G{len(logo)}>'.encode()+logo + esc)

        print('Done')

    def download_ttf_font(self, ttf_file_path: str, file_id: int):
        """ download TTF font to Boca printer """
        space_before = self._get_download_space_avail()
        if len(space_before) == 0:
            raise BocaTcpRespError("Boca <S7> got empty response!")

        with open(ttf_file_path, 'rb') as fp:
            ttf_font = fp.read()
            logger.info('Loaded TTF font to memory')
            self._sock.sendall(
                f'<ID{file_id}><ttf{len(ttf_font)}>'.encode()+ttf_font)

        space_after = self._get_download_space_avail()
        logger.info(
            f'Downloaded TTF font. Before/After spaces: {space_before} -> {space_after}')

    def _get_download_space_avail(self) -> str:
        """ Return bytes available on Boca storage """
        xmit_bytes = self._sock.send('<S7>'.encode())
        if xmit_bytes != 4:
            logger.error(
                'Transmitting <S7> but only {xmit_bytes=} went through')
        resp = self._sock.recvmsg(32)
        return resp[0]
