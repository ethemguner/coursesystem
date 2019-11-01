from django import template
register = template.Library()

@register.filter
def get_relate_to(i, relate_to):
    if relate_to == "1":
        relate_to = "Institution or Group 1"
    elif relate_to == "2":
        relate_to = "Institution or Group 2"
    elif relate_to == "3":
        relate_to = "External."
    else:
        relate_to = "Not defined! Please contact with a administrator."
    return relate_to