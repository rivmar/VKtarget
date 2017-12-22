
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^groups/', include('groups.urls', namespace='groups')),
    url(r'^admin/', admin.site.urls),
]
