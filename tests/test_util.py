from __future__ import (absolute_import)

import pytest

# add source dir to path.  Shouldn't tox take care of this for me?
import sys
sys.path.append('./src/samplemanager')


import uuid

from util import new_uid


def test_new_uid():
    assert isinstance(new_uid(), uuid.UUID)


if __name__ == '__main__':
    pytest.main()
