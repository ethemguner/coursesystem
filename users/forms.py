from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
import re


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=6, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label="Your password:", help_text="Min. 6 character.")
    password_confirm = forms.CharField(min_length=6,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label="Confirm password:")
    title = forms.ChoiceField(required=True, choices=Profile.TITLE, label="Institution or group relation:")
    phone = forms.CharField(widget=forms.TextInput, required=True, label="Phone number:")
    other_phone = forms.CharField(widget=forms.TextInput, required=False, label="Other phone number:")
    nationalid = forms.CharField(widget=forms.TextInput, required=True, label="ID Number:")
    first_name = forms.CharField(widget=forms.TextInput, required=True, max_length=75)
    last_name = forms.CharField(widget=forms.TextInput, required=True, max_length=75)

    class Meta:
        model = User
        fields = ['nationalid', 'first_name', 'last_name', 'username',
                  'password', 'password_confirm', 'email',
                  'title', 'phone', 'other_phone']
        labels = {'first_name': 'Your name:',
                  'last_name': 'Your last name:',
                  'username': 'Username:',
                  'email': 'E-mail:'}
        help_texts = {'email': "Enter an e-mail adress that you use currently.",
                      'username': 'Min. 6 character.'}

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '5xxxxxxxxx'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This e-mail adress is already in used.')
        return email

    def clean_nationalid(self):
        nationalid = self.cleaned_data.get('nationalid')
        try:
            int(nationalid)
        except:
            raise forms.ValidationError('Enter a valid ID number.')

        if len(nationalid) != 11:
            raise forms.ValidationError('Required 11 character.')

        if nationalid in User.objects.values_list('profile__nationalid', flat=True):
            raise forms.ValidationError('This ID number is already in used.')
        return nationalid

    def clean_username(self):
        username = self.cleaned_data.get('username')
        tr_characters = ["ğ", "Ğ", "ç", "Ç", "ş", "Ş", "ü", "Ü", "ö", "Ö", "ı", "İ"]

        for character in tr_characters:
            if character in username:
                raise forms.ValidationError('Cannot use "ğ,ç,ş,ü,ö,ı,İ"')

        if len(username) < 6:
            raise forms.ValidationError('Min. 6 character.')
        return username

class LoginForm(forms.Form):
    username = forms.CharField(label='ID Number, e-mail or your username:', required=True, max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'ID number, e-mail, username...'}))

    password = forms.CharField(label='Şifreniz:', required=True, max_length=50,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'password...'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            self.add_error('password', 'Invalid username/ID/e-mail or password.')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if re.match(r"[^@]+@[^@]+\.[^@]+", username):
            users = User.objects.filter(email__iexact=username)
            if len(users) > 0 and len(users) == 1:
                return users.first().username

        try:
            users = User.objects.all().values_list('profile__nationalid', flat=True)

            for nationalid in users:
                if username == nationalid:
                    user = Profile.objects.get(nationalid=username)
                    username = user.user.username
        except:
            self.add_error('username',"Couldn't defined this username.")

        return username

class UpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Document for Institution or group:",
                             help_text="""This document has to demonstrate your institution or group
                             relation. Also we're checking our users' document every one year.
                             After one year from upload date, this document will be invalid.
                             We'll inform you when update is needed for the document.""")
    title = forms.ChoiceField(required=True, choices=Profile.TITLE, label="Institution or group relation:")
    phone = forms.CharField(widget=forms.TextInput, required=True, label="Phone number:")
    other_phone = forms.CharField(widget=forms.TextInput, required=False, label="Other phone number:")
    nationalid = forms.CharField(widget=forms.TextInput, required=False, label="ID Number:")

    class Meta:
        model = User
        fields = ['nationalid', 'phone', 'other_phone', 'title', 'image']

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '5xxxxxxxxx'}
        self.fields['nationalid'].disabled = True
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone', None)
        try:
            int(phone_number)
            if len(phone_number) != 10 and phone_number[0] != "5":
                raise forms.ValidationError("Error! Format has to be 5xxxxxxxxx")
        except ValueError:
            raise forms.ValidationError("Please enter a phone number.")
        return phone_number


class PasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(min_length=6, required=True, label='Current password:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(min_length=6, required=True, label='New password:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                   help_text="Min. 6 character.")
    new_password_confirm = forms.CharField(min_length=6, required=True, label='Confirm new password:',
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            self.add_error('new_password', "Doesn't match.")
            self.add_error('new_password_confirm', "Doesn't match.")

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Your current password is wrong.")

        return old_password


class ForgotPasswordForm(forms.Form):
    nationalid = forms.IntegerField(required=False, label="ID Number:")

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean(self):
        nationalid = self.cleaned_data.get('nationalid', '')
        users = User.objects.all()
        if not str(nationalid) in users.values_list('profile__nationalid', flat=True):
            self.add_error('nationalid', 'We cannot find an account according to this ID number.')

        try:
            int(nationalid)
        except TypeError:
            self.add_error('nationalid', 'Invalid ID number.')