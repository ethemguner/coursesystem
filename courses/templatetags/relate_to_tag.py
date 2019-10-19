from django import template
register = template.Library()

@register.filter
def get_relate_to(i, relate_to):
    if relate_to == "1":
        relate_to = "Ege Üniversitesi öğrencisi / personeli / mezunu."
    elif relate_to == "2":
        relate_to = "Gazi / engelli / şehit yakını."
    elif relate_to == "3":
        relate_to = "Kurum dışı."
    else:
        relate_to = "Tanımlanamadı! Yetkili ile görüşün."
    return relate_to