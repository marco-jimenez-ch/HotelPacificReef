from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.habitaciones.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('reservas/', include('apps.reservas.urls')),
    path('pagos/', include('apps.pagos.urls')),
    path('panel/', include('apps.panel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
