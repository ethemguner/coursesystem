from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from courses.models import Course
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
import string
import random
from django.contrib.auth.models import User
from prereg.models import PreRegistration


def preregistrations(request):
    if request.user.is_staff:
        courses = Course.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'admin/preregs.html', context={'courses': courses})

def prereg_list(request, code):
    if request.user.is_staff:
        course = get_object_or_404(Course, course_code=code)
        who_app = course.prereg.values_list('user__username')
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'admin/who_applied.html', context={'who_app': who_app})


def send_payment_pages(request):
    if request.user.is_staff:
        data = {'is_valid': True}
        course_code = request.GET.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)
        mails_query = course.prereg.values_list('user__email', flat=True)

        # REGISTIRATION EXTENTION
        code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=25))
        course.registering_extension = code
        course.save()
        ext = course.registering_extension

        course.is_registerable = True
        course.save()

        course.status = '3'
        course.save()

        subject = "Ege UZEM | Başvurduğunuz kurs için kesin kayıtlar açılmıştır."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
        <h2 style="font-family: Trebuchet MS;">TALIMATLAR</h2>
        <p style="font-family: Calibri; font-size: 18px">Merhaba,</p>
        <p style="font-family: Calibri; font-size: 18px">
        Ödeme yapmak için aşağıdaki linke tıklayınız. Açılan sayfada ödeme yapmanız gereken hesabın gerekli
        bilgileri mevcuttur. Bu bilgiler doğrultusunda ödemeyi yapınız. Ödemeyi yapmadan önce lütfen bilgilerinizi
        "Bilgilerim" kısmından kontrol ediniz. Gerekli bilgileri/belgeleri doğru bir şekilde girdiğinizden
        emin olunuz.
        </p>

        <h2 style="font-family: Trebuchet MS;">ONAY SÜRESİ</h2>
        <p style="font-family: Calibri; font-size: 18px">
        Bilgileriniz tarafımıza ödemeyi yaptıktan sonra anında ulaşacaktır. Dekont, belge ve bilgilerinizde herhangi
        bir uyuşmazlık veya eksik yok ise kesin kaydınız 1-3 iş günü içerisinde onaylanır ve onay e-maili tarafınıza
        gönderilir.
        </p>

        <a href ="http://127.0.0.1:8000/payment/send-payment/{}" style="font-family: Bahnschrift; font-size: 20px;">
        Ödeme sayfasına gitmek için tıklayınız.
        </a>
        """.format(ext)

        counter = 0
        for mail in mails_query:
            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=False)
            counter += 1
            if counter == len(mails_query):
                messages.success(request, '{} adet e-mail gönderilmiştir.'.format(len(mails_query)),
                                 extra_tags="success")
            else:
                pass
    return JsonResponse(data=data)


def cancel_course(request):
    if request.user.is_staff:
        data = {'is_valid': True}
        course_code = request.GET.get('course_code')
        course = get_object_or_404(Course, course_code=course_code)
        mails_query = course.prereg.values_list('user__email', flat=True)

        code = ''.join(random.choices(string.ascii_lowercase +
                                      string.ascii_uppercase + string.digits, k=5))

        course.course_code = code
        course.status = '4'
        course.save()

        subject = "Ege UZEM | Başvurduğunuz kurs iptal edilmiştir."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
        <p style="font-family: Calibri Light;">Merhaba,</p>
        <p style="font-family: Calibri Light;">Ön başvuruda bulunduğunuz kurs yeterli katılım sağlanamadığından iptal edilmiştir.</p>
        <p style="font-family: Calibri Light;">Ekstra bir işlem yapmanıza gerek yoktur.</p>
        """
        counter = 0
        for mail in mails_query:
            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
            counter += 1
            user = get_object_or_404(User, email=mail)
            prereg = PreRegistration.objects.get(user=user)
            prereg.delete()
            if counter == len(mails_query):
                messages.success(request, '{} kişiye kurs iptal bilgisi gönderilmiştir.'.format(len(mails_query)),
                                 extra_tags="danger")
            else:
                pass
    return JsonResponse(data=data)

def close_registrations(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    data = {'is_valid':True}
    ext = request.GET.get('ext','')
    course = get_object_or_404(Course, registering_extension=ext)
    course.registering_extension = ""
    course.save()
    course.status = '1'
    course.save()
    return JsonResponse(data=data)



