from django.conf.urls import url
from .views import groups, group
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', groups, name='groups'),
    url(r'^group/$', group, name='group'),
    url(r'^group/(?P<pk>[0-9]+)/$', group, name='group'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)