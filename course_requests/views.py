from django.shortcuts import render, HttpResponseRedirect, reverse, get_object_or_404
from .forms import CourseGivenForm, CourseTakenForm
from .models import CourseGiven, CourseTaken
from django.contrib import messages
from django.http import JsonResponse

def course_given_request(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    form = CourseGivenForm(data=request.POST or None)

    if form.is_valid():
        title = form.cleaned_data.get('request_title')
        content = form.cleaned_data.get('request_content')
        max = form.cleaned_data.get('limit_max')
        min = form.cleaned_data.get('limit_min')
        user = request.user
        messages.success(request, 'Kurs verme talebiniz alınmıştır. Uygun görülürse sizinle iletişime geçilecektir.',
                         extra_tags='success')
        CourseGiven.objects.create(user=user, request_title=title, request_content=content, limit_max=max, limit_min=min).save()
        return HttpResponseRedirect(reverse('user-panel'))

    return render(request, 'course/requests/course-given-request.html', context={'form':form})

def course_taken_request(request):
    if not request.user.is_active:
        return HttpResponseRedirect(reverse('login'))
    form = CourseTakenForm(data=request.POST or None)

    if form.is_valid():
        title = form.cleaned_data.get('request_title')
        content = form.cleaned_data.get('request_content')
        user = request.user
        messages.success(request, 'Kurs alma talebiniz alınmıştır. Kurs açılırsa bilgi gönderilecektir.',
                         extra_tags='success')
        CourseTaken.objects.create(user=user, request_title=title, request_content=content).save()
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/requests/course-taken-request.html', context={'form':form})

def course_given_list(request):
    if request.user.is_staff:
        course_request = CourseGiven.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/requests/course-given-list.html', context={'course_request': course_request})

def course_taken_list(request):
    if request.user.is_staff:
        course_request = CourseTaken.objects.all()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return render(request, 'course/requests/course-taken-list.html', context={'course_request': course_request})

def delete_taken_request(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    if request.user.is_staff:
        data = {'is_valid':True}

        reqid = request.GET.get('reqid','')
        course = get_object_or_404(CourseTaken, id=reqid)
        course.delete()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return JsonResponse(data=data)

def delete_given_request(request):
    if not request.user.is_staff:
        return HttpResponseRedirect(reverse('user-panel'))
    if request.user.is_staff:
        data = {'is_valid':True}

        reqid = request.GET.get('reqid','')
        course = get_object_or_404(CourseGiven, id=reqid)
        course.delete()
    else:
        return HttpResponseRedirect(reverse('user-panel'))
    return JsonResponse(data=data)