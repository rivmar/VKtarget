from django.conf.urls import url
from .views import groups, group, files, get_token, auth


urlpatterns = [
    url(r'^$', groups, name='groups'),
    url(r'^group/$', group, name='group'),
    url(r'^group/(?P<pk>[0-9]+)/$', group, name='group'),
    url(r'^files/(?P<pk>[0-9]+)/$', files, name='files'),
    url(r'^token/$', get_token, name='get_token'),
    url(r'^auth/$', auth, name='auth'),
]
