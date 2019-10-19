from django.urls import path
from .views import course_given_request, course_taken_request, course_taken_list, delete_taken_request, \
    delete_given_request, course_given_list

urlpatterns = [
    path('given/', course_given_request, name="course-given-request"),
    path('taken/', course_taken_request, name="course-taken-request"),
    path('course-taken-list/', course_taken_list, name="course-taken-list"),
    path('course-given-list/', course_given_list, name="course-given-list"),
    path('delete-taken-request/', delete_taken_request, name="delete-taken-request"),
    path('delete-given-request/', delete_given_request, name="delete-given-request")
]