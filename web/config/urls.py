""" API URL Configuration """


from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


import debug_toolbar
from rest_framework_simplejwt import views as jwt_views


from apps.api import urls as api_urls, views as api_views


app_urls = [
    path("", include("django.contrib.auth.urls")),
    path("", include("apps.users.urls", namespace="users")),
    path("", include("apps.common.urls", namespace="common")),
    path("", include("apps.webhooks.urls", namespace="webhooks")),
]

api_urls = [
    path(
        "api/v1/token/refresh/",
        api_views.CustomTokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/",
        api_views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("api/v1/", include(api_urls, namespace="api")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urls)),
    path("", include(app_urls)),
    path("__debug__/", include(debug_toolbar.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "API Administration"
admin.site.site_title = "API Administration"
admin.site.index_title = "API Administration"
