=============================
spid_django
=============================

.. image:: https://badge.fury.io/py/spid-django.svg
    :target: https://badge.fury.io/py/spid-django

.. image:: https://travis-ci.org/italia/spid-django.svg?branch=master
    :target: https://travis-ci.org/italia/spid-django

.. image:: https://codecov.io/gh/italia/spid-django/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/italia/spid-django

SPID package for django application

Documentation
-------------

The full documentation is at https://spid-django.readthedocs.io.

Quickstart
----------

Install spid_django::

    pip install spid-django

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'spid_django.apps.SpidDjangoConfig',
        ...
    )

Add spid_django's URL patterns:

.. code-block:: python

    from spid_django import urls as spid_django_urls


    urlpatterns = [
        ...
        url(r'^', include(spid_django_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
