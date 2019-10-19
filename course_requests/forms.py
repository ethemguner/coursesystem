from django import forms
from .models import CourseTaken
from .models import CourseGiven

class CourseGivenForm(forms.ModelForm):
    class Meta:
        model = CourseGiven
        fields = ['request_title', 'limit_min', 'limit_max', 'request_content']
        labels = {
            'request_title': 'Kurs Tanımı:',
            'limit_min': 'Minimum kontenjan:',
            'limit_max': 'Maksimum kontenjan:',
            'request_content': 'Vermek istediğiniz kurs hakkında detaylar:'
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
                self.add_error('limit_max', 'Maksimum kontenjan, minimum kontenjandan küçük olamaz.')
        except TypeError:
            pass

class CourseTakenForm(forms.ModelForm):
    class Meta:
        model = CourseTaken
        fields = ['request_title', 'request_content']
        labels = {
            'request_title': 'Kurs Tanımı:',
            'request_content': 'Talep ettiğiniz kurs hakkında detaylar:'
        }

    def __init__(self, *args, **kwargs):
        super(CourseTakenForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['request_content'].widget.attrs['rows'] = 10