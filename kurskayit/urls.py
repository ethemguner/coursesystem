"""kurskayit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import users.urls
import Payments.urls
import courses.urls
import finalreg.urls
import course_requests.urls
from django.conf import settings
from django.conf.urls.static import static
from Payments.views import panel
from prereg.views import preregistrations, prereg_list, send_payment_pages, cancel_course, close_registrations
from users.views import deleting_images_page
from DateHolder.views import image_control
from Certification_Request.views import certificationrequest_list, upload_certificate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(users.urls)),
    path('payment/', include(Payments.urls)),
    path('course/', include(courses.urls)),
    path('finalregistration/', include(finalreg.urls)),
    path('course-request/', include(course_requests.urls)),
    path('panel/', panel, name="panel"),
    path('panel/pre-registrations/', preregistrations, name="preregs"),
    path('panel/course-requests/', panel, name="course-requests"),
    path('panel/pre-registrations/who-applied/<slug:code>', prereg_list, name="who-applied"),
    path('panel/send-mails/', send_payment_pages, name="send-mails"),
    path('panel/cancel-course/', cancel_course, name="cancel-course"),
    path('panel/close-registration/', close_registrations, name="close-registration"),
    path('panel/delete-images/', deleting_images_page, name='delete-images-page'),
    path('panel/delete-images/confirm/', image_control, name='image-control'),
    path('panel/certification-list/', certificationrequest_list, name='certification-list'),
    path('panel/upload-pdf/<slug:username>/<slug:course_code>/', upload_certificate, name='upload-certificate'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
