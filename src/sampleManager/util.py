import uuid

def new_uid():
    """
    Generate a new uid.
    """

    return uuid.uuid4()


def get_owner():
    """
    dummy stub for now, will eventually
    reliably/securely(?) determine the owner somehow.
    """

    return "skinner"


def run_on_empty(func, arg_list, arg_dict, key, **kwargs):
    """
    Check if 'key' exists in dictionary 'kwargs' and is not None or
    empty.  If not, run the specified function with the arg list and
    dictionary specified and return it's return value.
    
    return func(*arg_list, **arg_dict) if kwargs['key'] is:
        None
        ''
        or raises KeyError
    """

    try:
        if kwargs[key] is None or kwargs[key] == '':
            return func(*arg_list, **arg_dict)

    except KeyError:
        return func(*arg_list, **arg_dict)

