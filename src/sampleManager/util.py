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
