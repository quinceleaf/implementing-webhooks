from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, register_converter

from apps.common import converters
from apps.webhooks import views


register_converter(converters.ULIDConverter, "ulid")
app_name = "apps.webhooks"


urlpatterns = [
    path(
        "webhooks/partners/A1vb0fcen71q1cq25dcw8dqzc8gxuolgjbyfrX5ohpyQjlCAhcs3s5578f0w9Wcshykv2pD/",
        views.receive_webhook,
        name="webhook-partners",
    ),
]
