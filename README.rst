===============================
sampleManager
===============================

Sample Management Backend for NSLS2


dev:  |tci| |cvrg| |qual| |docs|

.. |tci| image:: https://travis-ci.org/cowanml/sampleManager.svg?branch=master
    :alt: Travis-CI Build Status - master
    :target: https://travis-ci.org/cowanml/sampleManager/branches


.. |cvrg| image:: https://coveralls.io/repos/cowanml/sampleManager/badge.png?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/cowanml/sampleManager?branch=master


.. |qual| image:: https://landscape.io/github/cowanml/sampleManager/master/landscape.svg
    :alt: Code Quality Status
    :target: https://landscape.io/github/cowanml/sampleManager/master


.. |docs| image:: https://readthedocs.org/projects/sampleManager/badge/?version=latest
    :alt: Documentation Status
    :target: http://sampleManager.readthedocs.org/en/latest


dev:  |tcidev| |cvrgdev| |qualdev| |docsdev|

.. |tcidev| image:: https://travis-ci.org/cowanml/sampleManager.svg?branch=dev
    :alt: Travis-CI Build Status - dev
    :target: https://travis-ci.org/cowanml/sampleManager/branches


.. |cvrgdev| image:: https://coveralls.io/repos/cowanml/sampleManager/badge.png?branch=dev
    :alt: Coverage Status
    :target: https://coveralls.io/r/cowanml/sampleManager?branch=dev


.. |qualdev| image:: https://landscape.io/github/cowanml/sampleManager/dev/landscape.svg
    :alt: Code Quality Status
    :target: https://landscape.io/github/cowanml/sampleManager/dev


.. |docsdev| image:: https://readthedocs.org/projects/sampleManager/badge/?version=dev
    :alt: Documentation Status
    :target: http://sampleManager.readthedocs.org/en/dev


Installation
============

Can't *pip* these yet :( ::

    git clone https://github.com/NSLS-II/sampleManager.git
    cd sampleManager
    python setup.py build && su -c python setup.py install


Documentation
=============

https://samplemanager.readthedocs.org/


Development
===========

Use `gitflow <https://github.com/nvie/gitflow#readme>`_.


To run tests::

    tox -e pep8
    tox -e flake8
    tox -e 2.7
    ...

