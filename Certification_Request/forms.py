from django import forms
from .models import Certificate

class CertificationRequestForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['user']

class CertificationUploadForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate']

    def __init__(self, *args, **kwargs):
        super(CertificationUploadForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}