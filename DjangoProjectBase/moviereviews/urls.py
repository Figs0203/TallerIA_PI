from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # This single line includes all URLs from your 'movie' app
    # and correctly registers the 'movie' namespace. This fixes the error.
    path('', include('movie.urls')),
]

# This is important for serving media files (like movie images) during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)