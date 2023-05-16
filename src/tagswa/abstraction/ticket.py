import abc

class Ticket(abc.ABC):
    """ Represent an event ticket """

    @classmethod
    @property
    @abc.abstractmethod
    def EVENTID(cls):
        raise NotImplementedError

    @abc.abstractmethod
    def build_boca_script(self) -> str:
        """ Translate ticket object into Boca printer FGL script """
    
    @staticmethod
    def split_long_line(line:str, char_per_line: int):
        """ split a string longer than char_per_line into multple lines """
        if len(line) <= char_per_line:
            return [line]

        tokens = line.split()
        num_tokens = len(tokens)
        sidx, eidx = (0, 0)
        lines = []
        cur_line_len = 0

        while eidx < num_tokens:
            token = tokens[eidx]
            if cur_line_len + len(token) + (eidx - sidx) <= char_per_line:
                cur_line_len += len(token)
                eidx += 1
            else:
                lines.append(' '.join(tokens[sidx:eidx]))
                sidx = eidx
                cur_line_len = 0

        if sidx < eidx:
            lines.append(' '.join(tokens[sidx:eidx]))

        return lines
