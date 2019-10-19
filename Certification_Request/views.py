from django.shortcuts import render, HttpResponseRedirect,reverse, get_object_or_404
from .models import Certificate
from django.contrib.auth.models import User
from .forms import CertificationUploadForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course
def certificationrequest_list(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    certification_requests = Certificate.objects.all()
    return render(request, 'admin/certification-list.html', context={'certifications':certification_requests})

def upload_certificate(request, username, course_code):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))

    user = get_object_or_404(User, username=username)
    course = get_object_or_404(Course, course_code=course_code)
    certificate = Certificate.objects.get(user=user, course=course)
    form = CertificationUploadForm(data=request.POST or None, files=request.FILES or None)

    if form.is_valid():
        file = form.cleaned_data.get('certificate','')
        certificate.certificate = file
        certificate.is_downloadable = True
        certificate.save()

        subject = "EGE UZEM | Sertifikanız yüklendi."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
            <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
            Sayın <b>{}</b>, talep ettiğiniz sertifika yüklendi.
            </p>
            <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
            <a href="http://127.0.0.1:8000/auth/login/">Buradan</a> giriş yaptıktan sonra ekranın sağ kısmındaki 
            "Kurslarım" tablosundaki "İNDİR & GÖRÜNTÜLE" yazısına tıklayınız.</p>
        """.format(user.get_full_name())

        send_mail(subject, message, from_mail, [user.email], html_message=html_msg, fail_silently=True)

        messages.success(request, 'Kullanıcının sertifikası yüklendi.', extra_tags='success')
        return HttpResponseRedirect(reverse('certification-list'))
    return render(request, 'admin/upload-pdf.html', context={'form':form, 'user':user, 'course_code':course_code})