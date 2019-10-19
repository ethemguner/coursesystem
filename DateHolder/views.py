from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from .models import DateHolder
from django.contrib.auth.models import User
import datetime
from dateutil import relativedelta as rdelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse

def image_control(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))

    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    #Today's date has defined.
    d1 = datetime.date(year, month, day)

    #For give message to admin that how much user's image has deleted
    deleted_images = []

    #Iterating users.
    users = User.objects.all()
    for user in users:
        try:
            date_h = DateHolder.objects.get(user=user)
            year = date_h.image_upload_date.year
            month = date_h.image_upload_date.month
            day = date_h.image_upload_date.day

            #The date which is image uploaded.
            d2 = datetime.date(year, month, day)

            #Difference between two date.
            x = rdelta.relativedelta(dt1=d1, dt2=d2)

            #If difference is 1 year or more.
            if x.years >= 1:
                user.profile.image = None
                user.profile.save()
                date_h.delete()
                deleted_images.append(user)
                email = user.email

                #Sending e-mail to user.
                subject = "EGE Uzem | Belgenizin geçerlilik süresi doldu."
                from_mail = settings.EMAIL_HOST_USER
                message = ""
                html_msg = """
                    <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                    Merhaba {},
                    </p>

                    <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                    <b>Ege Üniversitesi UZEM Kurs sistemindeki kayıtlı hesabınızda 
                    yüklemiş olduğunuz belgenin geçerlilik süresi dolmuştur.
                    </b>
                    </p>
                    <p style="font-family: 'Trebuchet MS'; font-size: 18px; font-color: red;">
                    <u>"Profilim" sekmesinden ilgili kurum bağlantınıza göre gerekli belgeyi güncellemeyi unutmayınız.</u><p/>
                    <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                    Ege Üniversitesi UZEM Kurs Kayıt Sistemine giriş yapmak için 
                    <a href="#">tıklayınız.</a></p>

                """.format(user.get_full_name())
                send_mail(subject, message, from_mail, [email], html_message=html_msg, fail_silently=True)
        except DateHolder.DoesNotExist:
            #If there is no dataholder object.
            pass

    if len(deleted_images) == 0:
        messages.success(request, 'Belge geçerlilik süresi dolmuş bir kullanıcı bulunamadı.',
                             extra_tags="danger")
    else:
        messages.success(request,
        '{} adet kullanıcının belgeleri silinmiş, e-maillerine bilgi gönderilmiştir.'.format(len(deleted_images)))
    return JsonResponse(data={'is_valid':True})
