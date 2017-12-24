from django.conf.urls import url
from .views import groups, group, files


urlpatterns = [
    url(r'^$', groups, name='groups'),
    url(r'^group/$', group, name='group'),
    url(r'^group/(?P<pk>[0-9]+)/$', group, name='group'),
    url(r'^files/(?P<pk>[0-9]+)/$', files, name='files'),
]
