from django.urls import path
from .views import detail, confirm, payment_gateaway
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('detail', detail, name="detail"),
    path('confirm', confirm, name="confirm"),
    path('send-payment/<slug:ext>', payment_gateaway, name="send-payment"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)