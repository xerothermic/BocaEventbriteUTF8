import itertools

def peek(it):
    """ Peek the first element and return the original iterator """
    try:
        first = next(it)
    except StopIteration:
        return None, None
    return first, itertools.chain([first], it)