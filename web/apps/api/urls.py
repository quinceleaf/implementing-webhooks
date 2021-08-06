from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter


from apps.api import views
from apps.common import converters as common_converters


register_converter(common_converters.ULIDConverter, "ulid")
app_name = "apps.api"


api_urls = [
    path("csrf/", views.get_csrf, name="api-csrf"),
    path("login/", views.login_view, name="api-login"),
    path("logout/", views.logout_view, name="api-logout"),
]

select_urls = []


urlpatterns = [
    path("select/", include(select_urls)),
    path("", include(api_urls)),
]
