from django.urls import path
from .views import user_login, user_logout, update_information, user_register, \
    user_panel, send_prereg, password_change, forgot_password

urlpatterns = [
    path('login/', user_login, name='login'),
    path('register/', user_register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('settings/', update_information, name='update'),
    path('user-panel/', user_panel, name='user-panel'),
    path('password-change/', password_change, name='password-change'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('application/send-app/<slug:code>', send_prereg, name='send-application'),

]