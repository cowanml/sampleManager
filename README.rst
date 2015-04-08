===============================
samplemanager
===============================

Sample Management Backend for NSLS2


master:  |tci| |cvrg| |qual| |docs|

.. |tci| image:: https://travis-ci.org/cowanml/samplemanager.svg?branch=master
    :alt: Travis-CI Build Status - master
    :target: https://travis-ci.org/cowanml/samplemanager/branches


.. |cvrg| image:: https://coveralls.io/repos/cowanml/samplemanager/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://coveralls.io/r/cowanml/samplemanager?branch=master


.. |qual| image:: https://landscape.io/github/cowanml/samplemanager/master/landscape.svg
    :alt: Code Quality Status
    :target: https://landscape.io/github/cowanml/samplemanager/master


.. |docs| image:: https://readthedocs.org/projects/samplemanager/badge/?version=latest
    :alt: Documentation Status
    :target: http://samplemanager.readthedocs.org/en/latest


dev:  |tcidev| |cvrgdev| |qualdev| |docsdev|

.. |tcidev| image:: https://travis-ci.org/cowanml/samplemanager.svg?branch=dev
    :alt: Travis-CI Build Status - dev
    :target: https://travis-ci.org/cowanml/samplemanager/branches


.. |cvrgdev| image:: https://coveralls.io/repos/cowanml/samplemanager/badge.svg?branch=dev
    :alt: Coverage Status
    :target: https://coveralls.io/r/cowanml/samplemanager?branch=dev


.. |qualdev| image:: https://landscape.io/github/cowanml/samplemanager/dev/landscape.svg
    :alt: Code Quality Status
    :target: https://landscape.io/github/cowanml/samplemanager/dev


.. |docsdev| image:: https://readthedocs.org/projects/samplemanager/badge/?version=dev
    :alt: Documentation Status
    :target: http://samplemanager.readthedocs.org/en/dev


Installation
============

Can't *pip* this yet :( ::

    git clone https://github.com/NSLS-II/samplemanager.git
    cd samplemanager
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

