from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
