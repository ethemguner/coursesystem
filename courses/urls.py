from django.urls import path
from .views import course_adding, course_list, course_edit, \
    active_courses, active_courses_detail, course_detail, course_discounts, send_certificationrequest, \
    course_user_list

urlpatterns = [
    path('course-add/', course_adding, name="course-add"),
    path('course-list/', course_list, name="course-list"),
    path('course-detail/<slug:code>', course_detail, name="course-detail"),
    path('course-edit/<slug:code>', course_edit, name="course-edit"),
    path('active-courses/', active_courses, name="active-courses"),
    path('active-courses/detail/<int:id>', active_courses_detail, name="active-courses-detail"),
    path('course-discount/', course_discounts, name="course-discount"),
    path('create-pdf/<int:pk>', send_certificationrequest, name="send-certificationrequest"),
    path('course-user-list/<slug:code>', course_user_list, name="course-user-list"),
]