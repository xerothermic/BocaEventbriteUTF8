import abc

class Boca(abc.ABC):
    """ Abstraction for Boca printer """
    @abc.abstractmethod
    def print(self, fgl_script: str):
        """ process print command """
