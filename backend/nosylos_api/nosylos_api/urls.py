from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django_ses.views import SESEventWebhookView
from user.urls import urlpatterns as user_url_patterns


urlpatterns = [
    path("argolis/", admin.site.urls),
    path("admin/django-ses/", include("django_ses.urls")),
    path(
        "ses/event-webhook/",
        SESEventWebhookView.as_view(),
        name="handle-event-webhook",
    ),
]

urlpatterns += user_url_patterns
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
