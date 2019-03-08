""" {{ project_name }} URL Configuration """
from django.conf import settings
from django.conf.urls import handler400, handler403, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url

from . import views


app_name = '{{ project_name }}'

urlpatterns = [
    url('admin/', admin.site.urls),
    path('', include('custom_auth.urls')),
    url('account/', include('allauth.urls')),
    url('avatar/', include('avatar.urls')),
    path('', views.IndexView.as_view(), name='index'),
]


handler400 = views.BadRequestView.as_view()
handler403 = views.PermissionDeniedView.as_view()
handler404 = views.PageNotFoundView.as_view()
handler500 = views.ServerErrorView.as_view()


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
