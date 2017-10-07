=====
Usage
=====

To use spid_django in a project, add it to your `INSTALLED_APPS`:

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
