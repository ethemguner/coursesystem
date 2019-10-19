from django import template
register = template.Library()
from finalreg.models import FinalRegistration
@register.filter
def finalregs_notifications(i):
    finalregs = FinalRegistration.objects.all().count()
    return finalregs