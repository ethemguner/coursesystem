from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from .forms import RegisterForm, LoginForm, UpdateForm, PasswordChangeForm, ForgotPasswordForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from courses.models import Course
from courses.forms import CourseCategoryForm
from prereg.models import PreRegistration
from Payments.models import Payment
from django.contrib.auth import update_session_auth_hash
import string
import random
from django.db.models import Q
from django.http import JsonResponse
from DateHolder.models import DateHolder
import datetime
from Certification_Request.models import Certificate

def user_register(request):
    if not request.user.is_active:
        form = RegisterForm(data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
            mail = form.cleaned_data.get('email', '')
            relate_to = form.cleaned_data.get('title', '')
            phone = form.cleaned_data.get('phone', '')
            other_phone = form.cleaned_data.get('other_phone', '')
            nationalid = form.cleaned_data.get('nationalid', '')

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            user.save()

            Profile.objects.create(user=user, title=relate_to, phone=phone, nationalid=nationalid,
                                   other_phone=other_phone).save()
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request,
                                     'Kaydınız başarıyla tamamlandı. E-mail adresinizi kontrol ediniz.',
                                     extra_tags="success")

                    subject = "EGE Uzem kaydınız alındı."
                    from_mail = settings.EMAIL_HOST_USER
                    message = ""
                    html_msg = """
                        <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                        Sayın <b>{}</b>, kaydınız başarılı bir şekilde oluşturuldu.
                        </p>
                        <p style="font-family: 'Trebuchet MS'; font-size: 17px;">
                        <a href="http://127.0.0.1:8000/auth/login/">Buradan</a> giriş yaptıktan sonra "Bilgilerim" kısmından 
                        kurum bağlantınıza göre belgenizi yükleyiniz. Aksi taktirde kurs başvurularında bulunamazsınız.</p>
                    """.format(request.user.get_full_name())

                    send_mail(subject, message, from_mail, [mail], html_message=html_msg, fail_silently=True)
                    return HttpResponseRedirect(reverse('panel'))
    else:
        return HttpResponseRedirect(reverse('panel'))
    return render(request, 'users/register.html', context={'form': form})


def user_login(request):
    if not request.user.is_active:
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    if request.user.is_staff:
                        return HttpResponseRedirect(reverse('panel'))
                loginMsg = "{}, hoşgeldiniz.".format(request.user.get_full_name())
                messages.success(request, loginMsg, extra_tags='success')
                return HttpResponseRedirect(reverse('user-panel'))
    else:
        return HttpResponseRedirect(reverse('user-panel'))

    return render(request, 'users/login.html', context={'form': form})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def update_information(request):
    if request.user.is_active:
        user = get_object_or_404(User, username=request.user.username)
        form = UpdateForm(instance=user.profile, data=request.POST or None, files=request.FILES or None)
        if form.is_valid():
            phone = form.cleaned_data.get('phone', None)
            relate_to = form.cleaned_data.get('title', None)
            nationalid = form.cleaned_data.get('nationalid', None)

            user.profile.phone = phone
            user.profile.relate_to = relate_to
            user.profile.nationalid = nationalid

            if user.profile.image:
                    if DateHolder.objects.filter(user=user).exists():
                        DateHolder.objects.get(user=user).delete()
                        DateHolder.objects.create(image_upload_date=datetime.datetime.now(), user=user).save()
                    else:
                        DateHolder.objects.create(image_upload_date=datetime.datetime.now(), user=user).save()
            else:
                pass

            user.profile.save()
            msg = "Bilgileriniz başarıyla güncellendi."
            messages.success(request, msg, extra_tags="success")
            return HttpResponseRedirect(reverse('user-panel'))
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'users/update.html', context={'user': user, 'form': form})

def user_panel(request):
    courses = []
    form = CourseCategoryForm(data=request.GET or None)

    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    else:
        all_courses = Course.objects.all()

        for course in all_courses:
            if course.status != '4':
                courses.append(course)

        if form.is_valid():
            category = form.cleaned_data.get('category')
            if category:
                temp_courses = all_courses.filter(Q(category__icontains=category))
                courses = []
                for course in temp_courses:
                    if course.status != '4':
                        courses.append(course)

        user = get_object_or_404(Profile, user=request.user)
        """
        try:
            certificate = Certificate.objects.get(user=request.user)
        except Certificate.DoesNotExist:
            certificate = None
        """

        user_courses = user.course.all()
    return render(request, 'users/user-panel.html', context={'courses': courses, 'user_courses': user_courses,
                                                             'form':form})

def send_prereg(request, code):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    else:
        course = get_object_or_404(Course, course_code=code)
        user = request.user
        preregs = PreRegistration.objects.filter(course=course)
        payments = Payment.objects.filter(course=course)

        for prereg in preregs:
            if user.username in prereg.user.username:
                messages.success(request, 'Bu kursa bir kere ön başvuruda bulunabilirsiniz.', extra_tags='danger')
                return HttpResponseRedirect(reverse('user-panel'))

        if payments.count() > 0:
            return HttpResponseRedirect(reverse('send-payment', kwargs={'ext': course.registering_extension}))
        else:
            if request.method == "POST":
                prereg = PreRegistration.objects.create(user=user)
                course.prereg.add(prereg)
                course.save()
                messages.success(request, 'Ön başvurunuz başarılı bir şekilde alınmıştır.')
                return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'apply-course.html', context={'course': course})

def password_change(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    else:
        form = PasswordChangeForm(user=request.user, data=request.POST or None)

        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Şifreniz başarıyla güncellendi.', extra_tags='success')
            return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'users/password-change.html', context={'form': form})

def forgot_password(request):
    global email
    form = ForgotPasswordForm(data=request.POST or None)

    if form.is_valid():
        nationalid = form.cleaned_data.get('nationalid', '')
        code = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6))
        users = User.objects.all().values_list('profile__nationalid', flat=True)
        for user_nationalid in users:
            if str(nationalid) == str(user_nationalid):
                profile = Profile.objects.get(nationalid=nationalid)
                email = profile.user.email
                profile.user.set_password(code)
                profile.user.save()

        subject = "EGE Uzem | Şifre yenileme talebi alındı."
        from_mail = settings.EMAIL_HOST_USER
        message = ""
        html_msg = """
            <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
            Şifre güncelleme talebinde bulunuldu. Aşağıdaki kod ile hesabınıza giriş yapabilirsiniz.
            </p>
                        
            <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
            <b>KOD: {}</b>
            </p>
            <p style="font-family: 'Trebuchet MS'; font-size: 18px; font-color: red;">
            <u>HESABINIZA GİRİŞ YAPTIKTAN SONRA "PROFİLİM" VE ARDINDAN "ŞİFRE DEĞİŞTİR" KISMINA TIKLAYIP
            ŞİFRENİZİ DEĞİŞTİRMEYİ UNUTMAYINIZ.</u><p/>
            
        """.format(code)
        send_mail(subject, message, from_mail, [email], html_message=html_msg, fail_silently=True)
        messages.success(request, 'Şifre yenilendi. E-mail adresinizi kontrol ediniz.')
        return HttpResponseRedirect(reverse('forgot-password'))
    return render(request, 'users/forgot_password.html', context={'form':form})

def confirm_delete_images(request):
    if not request.is_ajax():
        return HttpResponseRedirect(reverse('user-panel'))

    if request.user.is_staff:
        data = {'is_valid':True}
        users = User.objects.all()

        for user in users:
            user.profile.image = None
            user.profile.save()
            email = user.email

            subject = "EGE Uzem | Belgenizin geçerlilik süresi doldu."
            from_mail = settings.EMAIL_HOST_USER
            message = ""
            html_msg = """
                <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                Merhaba {},
                </p>
    
                <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                <b>Ege Üniversitesi UZEM Kurs sistemindeki kayıtlı hesabınızda yüklemiş olduğunuz belgenin geçerlilik
                süresi dolmuştur.
                </b>
                </p>
                <p style="font-family: 'Trebuchet MS'; font-size: 18px; font-color: red;">
                <u>"Profilim" sekmesinden ilgili kurum bağlantınıza göre gerekli belgeyi güncellemeyi unutmayınız.</u><p/>
                <p style="font-family: 'Trebuchet MS'; font-size: 18px;">
                Ege Üniversitesi UZEM Kurs Kayıt Sistemine giriş yapmak için 
                <a href="#">tıklayınız.</a></p>
                
                <p style="font-family: 'Trebuchet MS'; font-size: 18px; font-color: red;">
                İyi günler dileriz.<p/>
    
            """.format(user.get_full_name())
            send_mail(subject, message, from_mail, [email], html_message=html_msg, fail_silently=True)

            messages.success(request, 'İşlem başarılı. {} kullanıcıya işlem hakkında bilgi gönderildi.'.format(len(users)))
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return JsonResponse(data=data)

def deleting_images_page(request):
    if request.user.is_staff:
        users = User.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'admin/delete-images.html', context={'users': users})