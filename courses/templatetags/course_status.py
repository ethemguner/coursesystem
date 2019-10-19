from django import template
register = template.Library()

@register.filter
def get_status(i, course):
    if course == "1":
        course = "Devam ediyor."
    elif course == "2":
        course = "Ön kayıtlar açıldı."
    elif course == "3":
        course = 'Kesin kayıtlar açık.'
    elif course == "4":
        course = "Bitti."
    else:
        course = None
    return course