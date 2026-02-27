from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Blog app
    path('', include('blogpost.urls')),

    # Django Auth
    path('accounts/', include('django.contrib.auth.urls')),

    # Members app
    path('members/', include('members.urls')),
]

# ✅ SERVE MEDIA FILES IN DEVELOPMENT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)