from django import forms

class NoticeForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=True, label="Duyuru:")

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['message'].widget.attrs['rows'] = 10