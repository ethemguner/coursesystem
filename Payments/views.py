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
        messages.success(request, 'Bu kursa kaydolmak için zaten bir ödeme yaptınız.', extra_tags='danger')
        return HttpResponseRedirect(reverse('user-panel'))
    else:
        if form.is_valid():
            payment = Payment.objects.create(user=user, course=course)
            payment.account_owner = form.cleaned_data.get('account_owner')
            payment.price = form.cleaned_data.get('price')
            payment.image = form.cleaned_data.get('image')
            payment.save()

            subject = "Ege UZEM | Ödemeniz alınmıştır."
            from_mail = settings.EMAIL_HOST_USER
            message = ""
            mail = user.email
            html_msg = """
            <p style="font-family: Calibri Light; font-size: 20px;">Sayın {},</p>
            
            <p style="font-family: Calibri Light; font-size: 18px;">
            {} adlı kurs için yaptığınız ödeme bildirimi alınmıştır.
            </p>
            
            <p style="font-family: Calibri Light; font-size: 18px;">
            Ödemeniz 1-3 iş günü içerisinde kontrol edilecektir. Onaylandığında
            kursa kesin kaydınız gerçekleşecektir. Onay bilgisi e-mail adresinize gönderilecektir.
            </p>
            """.format(user.get_full_name(), course.name)

            send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
            messages.success(request, 'Ödeme bildiriminiz başarıyla gönderildi. E-mail adresinizde ödemeye ilişkin bilgiler gönderilmiştir.', extra_tags='success')
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
