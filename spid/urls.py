from django.conf.urls import url
from . import views

app_name = 'SPID'

urlpatterns = [
    url(r'^$', views.index,name='index'),
    url(r'^attrs/$', views.attrs, name='attrs'),
    url(r'^metadata/$', views.metadata, name='metadata'),
]
