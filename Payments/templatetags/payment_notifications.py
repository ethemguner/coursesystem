from django import template
from Payments.models import Payment
register = template.Library()

@register.filter
def get_notifications(i):
    notifications = Payment.objects.all().count()
    return notifications