# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from spid_django.urls import urlpatterns as spid_django_urls

urlpatterns = [
    url(r'^', include(spid_django_urls, namespace='spid_django')),
]
