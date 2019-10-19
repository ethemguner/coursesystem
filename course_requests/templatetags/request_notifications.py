from django import template
from course_requests.models import CourseTaken, CourseGiven
register = template.Library()

@register.filter
def request_notifications(i):
    taken_ones = CourseTaken.objects.all().count()
    given_ones = CourseGiven.objects.all().count()
    notification = taken_ones + given_ones
    return notification