import abc

class Ticket(abc.ABC):
    """ Represent an event ticket """

    @classmethod
    @property
    @abc.abstractmethod
    def EVENTID(cls):
        """ Eventbrite event id. Used to select derived ticket class. """
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
        if num_tokens == 1:
            return [line]

        lines = []
        cur_line = [tokens[0]]
        for token in tokens[1:]:
            cur_line_len = len(' '.join(cur_line))
            if cur_line_len + (1 + len(token)) <= char_per_line:
                cur_line.append(token)
            else:
                lines.append(' '.join(cur_line))
                cur_line = [token]

        if len(cur_line) > 0:
            lines.append(' '.join(cur_line))

        # sidx, eidx = (0, 0)

        # cur_line_len = 0

        # while eidx < num_tokens:
        #     token = tokens[eidx]
        #     if cur_line_len + len(token) + (eidx - sidx) <= char_per_line:
        #         cur_line_len += len(token)
        #         eidx += 1
        #     else:
        #         lines.append(' '.join(tokens[sidx:eidx]))
        #         sidx = eidx
        #         cur_line_len = 0

        # if sidx < eidx:
        #     lines.append(' '.join(tokens[sidx:eidx]))

        return lines
