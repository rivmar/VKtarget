from django.conf.urls import url
from .views import groups, create_group, update_group_contacts

urlpatterns = [
    url(r'^$', groups, name='groups'),
    url(r'^add/$', create_group, name='add'),
    url(r'^update/(?P<pk>[0-9]+)/$', update_group_contacts, name='update'),
]