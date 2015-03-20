from __future__ import (absolute_import)

import pytest

from .util import new_uid


def test_new_uid():
    assert isinstance(new_uid(), uuid.UUID)


if __name__ == '__main__':
    pytest.main()
