from django import template
register = template.Library()

@register.filter
def get_status(i, course):
    if course == "1":
        course = "Continuing."
    elif course == "2":
        course = "Pre-registration open."
    elif course == "3":
        course = 'Final registration open.'
    elif course == "4":
        course = "Finished."
    else:
        course = None
    return course