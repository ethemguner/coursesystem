from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Course, CourseDiscount
from .forms import CourseAddingForm
import string, random
from finalreg.models import FinalRegistration
from .forms import CourseDiscountForm
from django.contrib import messages
from Certification_Request.models import Certificate
import datetime
from dateutil import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
import os
from django.http import JsonResponse

def course_adding(request):
    if request.user.is_staff:
        form = CourseAddingForm(data=request.POST or None)

        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            course = get_object_or_404(Course, name=name)

            code = ''.join(random.choices(string.ascii_lowercase +
                                          string.ascii_uppercase + string.digits, k=5))
            course.course_code = code

            if course.status == "3":
                course.status = "2"
                course.is_registerable = False
            else:
                pass
            course.save()
            return HttpResponseRedirect(reverse('panel'))
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/course-add.html', context={'form':form})

def course_edit(request, code):
    if request.user.is_staff:
        course = get_object_or_404(Course, course_code=code)
        form = CourseAddingForm(instance=course, data=request.POST or None)

        if form.is_valid():
            status = form.cleaned_data.get('status', '')
            if status == "3":
                course.is_registerable = True
                ext = ''.join(random.choices(string.ascii_lowercase +
                                              string.ascii_uppercase + string.digits, k=25))
                course.registering_extension = ext
                course.save()
            else:
                course.is_registerable = False
                code = ''.join(random.choices(string.ascii_lowercase +
                                              string.ascii_uppercase + string.digits, k=5))
                course.course_code = code
                course.save()

            form.save()
            return HttpResponseRedirect(reverse('panel'))
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/course-edit.html', context={'form':form})

def course_list(request):
    if request.user.is_staff:
        courses = Course.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/course-list.html', context={'courses':courses})

def active_courses(request):
    if request.user.is_staff:
        finalregs = FinalRegistration.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/active-courses.html', context={'finalregs':finalregs})

def course_detail(request, code):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    else:
        course = get_object_or_404(Course, course_code=code)
    return render(request, 'course/course-detail.html', context={'course':course})

def course_discounts(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    if request.user.is_staff:
        form = CourseDiscountForm(data=request.POST or None)
        discount = CourseDiscount.objects.get(id=2)
        if form.is_valid():
            d1 = form.cleaned_data.get('discount_1')
            d2 = form.cleaned_data.get('discount_2')
            account_info = form.cleaned_data.get('bank_info')
            discount.discount_1 = d1
            discount.discount_2 = d2

            if len(account_info) == 0:
                messages.success(request, 'Discount applied', extra_tags='success')
            else:
                discount.bank_info = account_info
                messages.success(request, 'Bank account information and discounts updated.', extra_tags='success')

            discount.save()
            return HttpResponseRedirect(reverse('course-discount'))
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/discount-edit.html', context={'form':form, 'discount':discount})

def send_certificationrequest(request, pk):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    else:
        course = get_object_or_404(Course, id=pk)

        today = datetime.date(datetime.datetime.now().year,
                              datetime.datetime.now().month,
                              datetime.datetime.now().day)

        c_date  =course.finish_at
        c_finishing_date = datetime.date(c_date.year,
                                         c_date.month,
                                         c_date.day)

        diff = relativedelta.relativedelta(today, c_finishing_date)
        diff_tuple = diff.years, diff.months, diff.days
        if diff_tuple[0] >= 0 and diff_tuple[1] >= 0 and diff_tuple[2] >= 0:
            if Certificate.objects.filter(user=request.user, course=course).exists():
                messages.success(request, "You've already sent a request. "
                                          "Please wait until we upload your certification.",
                                 extra_tags='danger')
                return HttpResponseRedirect(reverse('user-panel'))
            else:
                Certificate.objects.create(user=request.user, course=course).save()
                subject = "Course | A new certification request has taken."
                from_mail = settings.EMAIL_HOST_USER
                message = ""
                html_msg = """
                    <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                    Please check certification request on "Certification Requests" from management panel.
                    </p>
                """

                send_mail(subject, message, from_mail, [os.environ['EMAIL_ADRESS']], html_message=html_msg, fail_silently=True)
            messages.success(request,
                    'Your certification request has taken. When we upload your certification, we will send a e-mail.')
        else:
            messages.success(request, 'You cannot send a request for an unfinished course.', extra_tags="danger")
    return HttpResponseRedirect(reverse('user-panel'))

def course_user_list(request, code):
    course = get_object_or_404(Course, course_code=code)
    users = course.profile_set.all()
    return render(request, 'course/course-user-list.html', context={'users':users})

def user_contact_info(request):
    data = {'is_valid': True, 'name': '', 'mail': '', 'phone': '', 'other_phone': ''}

    name = request.GET.get('name')
    mail = request.GET.get('mail')
    phone = request.GET.get('phone')
    other_phone = request.GET.get('other_phone')

    data.update({'name': name, 'mail': mail, 'phone': phone, 'other_phone': other_phone})
    return JsonResponse(data=data)