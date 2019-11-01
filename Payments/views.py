from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Payment
from .forms import PaymentForm
from django.contrib.auth.models import User
from courses.models import Course
from users.models import Profile
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

def payment_gateaway(request, ext):
    form = PaymentForm(data=request.POST or None, files=request.FILES or None)
    course = get_object_or_404(Course, registering_extension=ext)
    user = get_object_or_404(User, username=request.user.username)
    profile = get_object_or_404(Profile, user=user)
    payments = Payment.objects.filter(course=course)

    if user.username in payments.values_list('user__username', flat=True):
        messages.success(request, 'You already have this course or you have sent the payment.', extra_tags='danger')
        return HttpResponseRedirect(reverse('user-panel'))
    else:
        if form.is_valid():
            payment = Payment.objects.create(user=user, course=course)
            payment.account_owner = form.cleaned_data.get('account_owner')
            payment.price = form.cleaned_data.get('price')
            payment.image = form.cleaned_data.get('image')
            payment.save()

            subject = "Course | We've received your payment."
            from_mail = settings.EMAIL_HOST_USER
            message = ""
            mail = user.email
            html_msg = """
            <p style="font-family: Calibri Light; font-size: 20px;">Dear {},</p>
            
            <p style="font-family: Calibri Light; font-size: 18px;">
            We've received your payment for {}.
            </p>
            
            <p style="font-family: Calibri Light; font-size: 18px;">
            We'll check your payment and verify your registration. It may take at least 1 day to done.
            </p>
            """.format(user.get_full_name(), course.name)

            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
            messages.success(request, 'Your payment has sent successfully. '
                                      'Your registration will be verify in 24 hours.', extra_tags='success')
            return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'payments.html', context={'course': course, 'form': form, 'profile': profile})


def panel(request):
    if request.user.is_staff:
        payments = Payment.objects.all()
        amount = Payment.objects.all().count()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'admin/panel.html', context={'payments': payments, 'amount': amount})


def detail(request):
    data = {'is_valid': True, 'name': '', 'mail': '', 'phone': '', 'other_phone': ''}

    name = request.GET.get('name')
    mail = request.GET.get('mail')
    phone = request.GET.get('phone')
    other_phone = request.GET.get('other_phone')

    data.update({'name': name, 'mail': mail, 'phone': phone, 'other_phone': other_phone})
    return JsonResponse(data=data)


def confirm(request):
    data = {'is_valid': True}

    payment_id = request.GET.get('payment_id')
    payment_user = request.GET.get('payment_user')
    course_code = request.GET.get('course_code')

    course = get_object_or_404(Course, course_code=course_code)
    user = get_object_or_404(User, username=payment_user)
    profile = get_object_or_404(Profile, user=user)
    profile.course.add(course)
    profile.save()

    payment = get_object_or_404(Payment, id=payment_id)
    payment.delete()
    return JsonResponse(data=data)
