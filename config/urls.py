from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("projects/", include("apps.projects.urls")),
    path("tasks/", include("apps.tasks.urls")),
    path("", RedirectView.as_view(pattern_name="projects:list"), name="home"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
