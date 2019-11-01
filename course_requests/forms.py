from django import forms
from .models import CourseTaken
from .models import CourseGiven

class CourseGivenForm(forms.ModelForm):
    class Meta:
        model = CourseGiven
        fields = ['request_title', 'limit_min', 'limit_max', 'request_content']
        labels = {
            'request_title': 'Course title:',
            'limit_min': 'Min. quota:',
            'limit_max': 'Max. quota:',
            'request_content': 'Details about course that you want to give:'
        }

    def __init__(self, *args, **kwargs):
        super(CourseGivenForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['request_content'].widget.attrs['rows'] = 10


    def clean(self):
        limit_max = self.cleaned_data.get('limit_max')
        limit_min = self.cleaned_data.get('limit_min')
        try:
            if limit_max < limit_min:
                self.add_error('limit_max', 'Max. quota cannot be lower than min. quota.')
        except TypeError:
            pass

class CourseTakenForm(forms.ModelForm):
    class Meta:
        model = CourseTaken
        fields = ['request_title', 'request_content']
        labels = {
            'request_title': 'Course title:',
            'request_content': 'Details about course that you want to take:'
        }

    def __init__(self, *args, **kwargs):
        super(CourseTakenForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['request_content'].widget.attrs['rows'] = 10