import json
from types import SimpleNamespace as Namespace

def gen_obj(data):
    """ Convert a JSON object to a Python object """
    if isinstance(data, dict):
        data = json.dumps(data)
    return json.loads(data, object_hook=lambda d: Namespace(**d))
