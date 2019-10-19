from django.urls import path
from .views import confirm_finalreg, cancel_finalreg, export_users_xls, finalreg_sendmail


urlpatterns = [
    path('confirm-finalreg/', confirm_finalreg, name="confirmFinalReg"),
    path('cancel-finalreg/', cancel_finalreg, name="cancelFinalReg"),
    path('create-excel/', export_users_xls, name="create-excel"),
    path('send-notice/<slug:code>', finalreg_sendmail, name="send-notice")
]