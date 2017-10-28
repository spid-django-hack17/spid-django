from django.conf.urls import url
from . import views

app_name = 'SPID'

urlpatterns = [
    url(r'^metadata/$', views.metadata, name='metadata'),
]
