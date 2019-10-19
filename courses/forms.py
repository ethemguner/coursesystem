from django import forms
from .models import Course, CourseDiscount

class CourseAddingForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'start_at', 'finish_at', 'price', 'category','status', 'content']
        labels = {
            'name':'Kurs İsmi:',
            'start_at':'Başlangıç tarihi:',
            'finish_at':'Bitiş tarihi:',
            'price':'Ücreti:',
            'category':'Kurs kategori:',
            'status':'Kurs Durumu:',
            'content':'Kurs İçeriği:'
        }

    def __init__(self, *args, **kwargs):
        super(CourseAddingForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['content'].widget.attrs['rows'] = 10

class CourseDiscountForm(forms.ModelForm):
    class Meta:
        model = CourseDiscount
        fields = ['discount_1', 'discount_2', 'bank_info']

    def __init__(self, *args, **kwargs):
        super(CourseDiscountForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['bank_info'].widget.attrs['rows'] = 10

    def clean(self):
        discount_1 = self.cleaned_data.get('discount_1')
        discount_2 = self.cleaned_data.get('discount_2')

        if int(discount_1) < 0 or int(discount_2) < 0:
            raise forms.ValidationError('Negatif değer girilemez.')

class CourseCategoryForm(forms.Form):
    CATEGORIES = (
        (None, 'Seçiniz'),
        ('1', 'Senkron'),
        ('2', 'Asenkron')
    )
    category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
                                     choices=CATEGORIES, required=False, label="Kategori Filtrele:")