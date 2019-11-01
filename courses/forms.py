from django import forms
from .models import Course, CourseDiscount

class CourseAddingForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'start_at', 'finish_at', 'price', 'category','status', 'content']
        labels = {
            'name':'Course Name:',
            'start_at':'Start at:',
            'finish_at':'Finish at:',
            'price':'Price:',
            'category':'Course category:',
            'status':'Course status:',
            'content':'Course content:',
        }

    def __init__(self, *args, **kwargs):
        super(CourseAddingForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['start_at'].widget.attrs = {'class': 'form-control', 'placeholder':'MM/DD/YYYY HH:MM'}
            self.fields['finish_at'].widget.attrs = {'class': 'form-control', 'placeholder':'MM/DD/YYYY HH:MM'}
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
            raise forms.ValidationError('Cannot insert a negative input.')

class CourseCategoryForm(forms.Form):
    CATEGORIES = (
        (None, 'Choose'),
        ('1', 'Senkron'),
        ('2', 'Asenkron')
    )
    category = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}),
                                     choices=CATEGORIES, required=False, label="Category filter:")