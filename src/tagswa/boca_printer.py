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

    def print_logo_inline(self, logo_file_path: str, row: int = 0, col: int = 0):
        """ Print a 1-bit BMP at (row, col) without storing it on the printer.

        Sends <SP{row},{col}><bmp><G{size}>{bmp_bytes}<p>. Useful for quick
        tests or one-off prints. For repeated use of the same logo, prefer
        download_logo() + <LD{slot}> to avoid re-sending the bytes each time.
        """
        with open(logo_file_path, 'rb') as fp:
            bmp = fp.read()
        header = f'<SP{row},{col}><bmp><G{len(bmp)}>'.encode()
        self._sock.sendall(header + bmp + b'<p>')
        logger.info(f'Printed inline {logo_file_path} ({len(bmp)} bytes) at RC{row},{col}')

    def download_logo(self, logo_file_path: str, logo_id: int):
        """ Download a 1-bit BMP logo into slot logo_id on the printer.

        After calling this, the logo can be referenced in FGL scripts via
        <SP{row},{col}><LD{logo_id}>. The printer needs ~30 seconds to
        commit the data to flash before the slot becomes usable. Monitor
        the printer LCD panel and wait until it shows "DOWNLOAD OK!"
        before issuing any <LD{logo_id}> recall.
        """
        with open(logo_file_path, 'rb') as fp:
            logo = fp.read()
        logger.info(f'{logo_file_path=} ({len(logo)} bytes) -> slot {logo_id}')

        esc = chr(27).encode()
        self._sock.sendall(
            esc + f'<ID{logo_id}><bmp><G{len(logo)}>'.encode() + logo + esc)
        logger.info(f'Downloaded. Wait for printer LCD "DOWNLOAD OK!" before <LD{logo_id}>.')

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
