from django.shortcuts import get_object_or_404, render, HttpResponseRedirect, reverse
from django.contrib.auth.models import User
from Payments.models import Payment
from courses.models import Course
from .models import FinalRegistration
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
import datetime
from .forms import NoticeForm
import xlwt
from users.models import Profile
from prereg.models import PreRegistration

def confirm_finalreg(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    data = {'is_valid': True}

    # DATA TAKEN.
    username = request.GET.get('username')
    payment_id = request.GET.get('payment_id')
    course_code = request.GET.get('course_code')

    # REQUIRED OBJECTS DEFINED FOR FINALREGISTRATION.
    user = get_object_or_404(User, username=username)
    payment = get_object_or_404(Payment, id=payment_id)

    course = get_object_or_404(Course, registering_extension=course_code)

    # ADDING COURSE TO USER'S COURSE OBJECT.
    user.profile.course.add(course)
    # CREATING FINALREGISTRATION.
    FinalRegistration.objects.create(user=user, course=course, payment=payment)

    course_start_at = "{}/{}/{}".format(course.start_at.day, course.start_at.month, course.start_at.year)
    course_finish_at = "{}/{}/{}".format(course.finish_at.day, course.finish_at.month, course.finish_at.year)

    # PREPARING MAIL'S ATTRIBUTES.
    subject = "Ege UZEM | Kurs kesin kaydınız gerçekleşmiştir.."
    from_mail = settings.EMAIL_HOST_USER
    message = ""
    mail = user.email
    html_msg = """
    <p style="font-family: Calibri Light; font-size: 20px;">Sayın {},</p>
    <p style="font-family: Calibri Light; font-size: 18px;">{} adlı kursa kesin kaydınız gerçekleşmiştir.</p>
    <p style="font-family: Calibri Light; font-size: 18px;">Kursunuz {} ila {} tarihleri arasında gerçekleşecektir.</p>
    """.format(user.get_full_name(), course.name, course_start_at, course_finish_at)

    # SENDING.
    send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)

    # MESSAGE TO ADMIN.
    messages.success(request, '{} e-mail adresinize kesin kayıt bilgisi gönderilmiştir.'.format(user.email),
                     extra_tags='success')

    return JsonResponse(data=data)


def cancel_finalreg(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    data = {'is_valid': True}

    # DATA TAKEN.
    username = request.GET.get('username')
    course_code = request.GET.get('course_code')

    user = get_object_or_404(User, username=username)
    payment = get_object_or_404(Payment, user=user)
    course = get_object_or_404(Course, registering_extension=course_code)
    prereg = get_object_or_404(PreRegistration, user=user)

    prereg.delete()
    payment.delete()

    subject = "Ege UZEM | Kesin kaydınız için yaptığınız ödeme reddedilmiştir."
    from_mail = settings.EMAIL_HOST_USER
    message = ""
    mail = user.email
    html_msg = """
    <p style="font-family: Calibri Light; font-size: 20px;">Sayın {},</p>
    <p style="font-family: Calibri Light; font-size: 18px;">{} adlı kurs için yaptığınız ödeme reddedilmiştir.</p>
    <p style="font-family: Calibri Light; font-size: 18px;">
    Ödemeniz reddedilmesi hakkında gerekli bilgiler e-mail adresinize kısa bir süre içerisinde bildirilecektir.
    </p>
    """.format(user.get_full_name(), course.name)

    send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
    messages.success(request, '{} e-mail adresinize ret bilgisi gönderilmiştir.'.format(user.email),
                     extra_tags='danger')

    return JsonResponse(data=data)


def export_users_xls(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="KesinKayitlarListesi_{}.xls"'.format(
        datetime.datetime.now())

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Kesin_Kayitlar')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Adı', 'Soyadı', 'Kursu', 'Ödediği Tutar', 'E-mail', 'Tel no.']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = FinalRegistration.objects.all().values_list('user__first_name', 'user__last_name', 'course__name',
                                                       'payment__course__price', 'user__email', 'user__profile__phone')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def finalreg_sendmail(request, code):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    course = get_object_or_404(Course, course_code=code)
    profiles = Profile.objects.filter(course=course)
    mails = profiles.values_list('user__email', flat=True)
    mails = list(dict.fromkeys(mails))
    form = NoticeForm(data=request.POST or None)

    if form.is_valid():
        msg = form.cleaned_data.get('message', '')

        subject = "Ege UZEM | Yeni Duyuru"
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
        <h2 style="font-family: 'Trebuchet MS';>DUYURU</h2>
        <p style="font-family: 'Calibri Light'; font-size= 18px;">{}</p>
        <p>Ege Üni. UZEM tarafından gönderilmiştir.</p>
        """.format(msg)

        for mail in mails:
            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=False)
        messages.success(request, 'Duyuru {} kişiye başarıyla gönderildi.'.format(len(mails)), extra_tags='success')
    return render(request, 'admin/send-notice.html', context={'form': form, 'course_code':code, 'profiles':profiles})