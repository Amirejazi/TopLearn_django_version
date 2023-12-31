from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home.urls')),
    path('account/', include('apps.accounts.urls', namespace='accounts')),
    path('userpanel/', include('apps.userpanel.urls', namespace='userpanel')),
    path('payment/', include('apps.payment.urls', namespace='payment')),
    path('course/', include('apps.course.urls', namespace='course')),
    path('order/', include('apps.order.urls', namespace='order')),
    path('forum/', include('apps.forum.urls', namespace='forum')),

    path('ckeditor', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "مدیریت Toplearn"