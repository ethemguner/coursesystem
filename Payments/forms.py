from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Receipt:")
    class Meta:
        model = Payment
        fields = ['account_owner', 'image']
        labels = {
            'account_owner':'Who made the transaction:'
        }

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields[field].widget.attrs['rows'] = 10