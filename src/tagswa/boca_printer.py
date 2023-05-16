import logging
import socket
from tagswa.abstraction.ticket import Ticket

logger = logging.getLogger(__name__)

class BocaTcpRespError(Exception):
    """ Represent Boca printer tcp response error """
    pass

class BocaTcpPrinter:
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

    def download_ttf_font(self, ttf_file_path: str, file_id: int):
        """ download TTF font to Boca printer """
        space_before = self._get_download_space_avail()
        if len(space_before) == 0:
            raise BocaTcpRespError("Boca <S7> got empty response!")

        with open(ttf_file_path, 'rb') as fp:
            ttf_font = fp.read()
            logger.info('Loaded TTF font to memory')
            self._sock.sendall(f'<ID{file_id}><ttf{len(ttf_font)}>'.encode()+ttf_font)

        space_after = self._get_download_space_avail()
        logger.info(f'Downloaded TTF font. Before/After spaces: {space_before}/{space_after}')

    def _get_download_space_avail(self) -> str:
        """ Return bytes available on Boca storage """
        orig_timeout_val = self._sock.gettimeout()
        logger.debug(f"Original socket timeout value:{orig_timeout_val}")
        # Shorten the timeout value to improve responsiveness
        self._sock.settimeout(1.5)
        self._sock.sendall('<S7>'.encode())
        resp = []
        try:
            while True:
                ch = self._sock.recv(1)
                resp.append(ch)
        except socket.timeout:
            pass

        return ''.join(resp)
