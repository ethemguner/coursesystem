from django import template
from django.conf import settings
from courses.models import CourseDiscount
register = template.Library()

@register.filter
def discount_1(i, price):
    discount = CourseDiscount.objects.get(id=2)
    x = (price / 100) * discount.discount_1
    y = price - x
    return y

@register.filter
def discount_2(i, price):
    discount = CourseDiscount.objects.get(id=2)
    x = (price / 100) * discount.discount_2
    y = price - x
    return y

@register.filter
def get_bank(i):
    discount = CourseDiscount.objects.get(id=2)
    bank_info = discount.bank_info
    return bank_info