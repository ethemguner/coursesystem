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

        subject = "Course | Final registrations have started."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
        <h2 style="font-family: Trebuchet MS;">INSTRUCTIONS</h2>
        <p style="font-family: Calibri; font-size: 18px">Hello,</p>
        <p style="font-family: Calibri; font-size: 18px">
        To pay, click link below. On the opening page, you'll see bank account information.
        According to these information make the payment. Before paying, check your information
        from "My Profile". Be sure you've the document and other information.
        </p>

        <h2 style="font-family: Trebuchet MS;">Verification Period</h2>
        <p style="font-family: Calibri; font-size: 18px">
        When you sent the payment, we'll check it and If everything is fine, your certain registration will be done.
        </p>

        <a href ="http://127.0.0.1:8000/payment/send-payment/{}" style="font-family: Bahnschrift; font-size: 20px;">
        Click to go payment page.
        </a>
        """.format(ext)

        counter = 0
        for mail in mails_query:
            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=False)
            counter += 1
            if counter == len(mails_query):
                messages.success(request, '{} e-mail sent for final registration.'.format(len(mails_query)),
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

        subject = "Course | Course has been declined."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
        <p style="font-family: Calibri Light;">Hello,</p>
        <p style="font-family: Calibri Light;">Not enough participation for course that you applied.</p>
        <p style="font-family: Calibri Light;">Check the other courses.</p>
        """
        counter = 0
        for mail in mails_query:
            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
            counter += 1
            user = get_object_or_404(User, email=mail)
            prereg = PreRegistration.objects.get(user=user)
            prereg.delete()
            if counter == len(mails_query):
                messages.success(request, '{} e-mail sent successfully.'.format(len(mails_query)),
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



