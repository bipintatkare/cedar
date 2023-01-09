from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("backend.urls")),

    path("", include("frontend.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
