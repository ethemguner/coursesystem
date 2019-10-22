from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
import re


class RegisterForm(forms.ModelForm):
    password = forms.CharField(min_length=6, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               label="Şifreniz:", help_text="En az 6 karakter.")
    password_confirm = forms.CharField(min_length=6,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                       label="Şifre onay:")
    title = forms.ChoiceField(required=True, choices=Profile.TITLE, label="Kurum bağlantınız:")
    phone = forms.CharField(widget=forms.TextInput, required=True, label="Telefon numaranız:")
    other_phone = forms.CharField(widget=forms.TextInput, required=False, label="Diğer tel. numaranız:")
    nationalid = forms.CharField(widget=forms.TextInput, required=True, label="T.C Kimlik Numaranız:")
    first_name = forms.CharField(widget=forms.TextInput, required=True, max_length=75)
    last_name = forms.CharField(widget=forms.TextInput, required=True, max_length=75)

    class Meta:
        model = User
        fields = ['nationalid', 'first_name', 'last_name', 'username',
                  'password', 'password_confirm', 'email',
                  'title', 'phone', 'other_phone']
        labels = {'first_name': 'Adınız:',
                  'last_name': 'Soyadınız:',
                  'username': 'Kullanıcı adınız:',
                  'email': 'E-mail adresiniz:'}
        help_texts = {'email': "Aktif olarak kullandığınız bir e-mail adresi giriniz.",
                      'username': 'En az 6 karakter. Türkçe karakter içeremez.'}

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
            self.fields['phone'].widget.attrs = {'class': 'form-control', 'placeholder': '5xxxxxxxxx'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email = email.lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Bu e-mail zaten kayıtlı.')
        return email

    def clean_nationalid(self):
        nationalid = self.cleaned_data.get('nationalid')
        try:
            int(nationalid)
        except:
            raise forms.ValidationError('Geçerli bir kimlik numarası giriniz.')

        if len(nationalid) != 11:
            raise forms.ValidationError('11 karakter gereklidir.')

        if nationalid in User.objects.values_list('profile__nationalid', flat=True):
            raise forms.ValidationError('Bu T.C Kimlik No ile bir kayıt zaten yapılmıştır.')
        return nationalid

    def clean_username(self):
        username = self.cleaned_data.get('username')
        tr_characters = ["ğ", "Ğ", "ç", "Ç", "ş", "Ş", "ü", "Ü", "ö", "Ö", "ı", "İ"]

        for character in tr_characters:
            if character in username:
                raise forms.ValidationError('Türkçe karakter içeremez.')

        if len(username) < 6:
            raise forms.ValidationError('En az 6 karakter gereklidir.')
        return username

class LoginForm(forms.Form):
    username = forms.CharField(label='T.C Kimlik, kullanıcı adı veya e-mail adresiniz:', required=True, max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'T.C Kimlik, kullanıcı adı, e-mail adresi...'}))

    password = forms.CharField(label='Şifreniz:', required=True, max_length=50,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'placeholder': 'şifre...'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if not user:
            self.add_error('password', 'Hatalı şifre veya kullanıcı adı.')

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
            self.add_error('username','Kullanıcı adı tanımlanamadı.')

        return username

class UpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="Kurum bağlantınıza ilişkin belge:",
                             help_text="""Belgenizin güncel kalması amacı 
                             ile belirli aralıklarla belge kontrolü yapmaktayız. Kontrol
                             yapıldığında belgenizin yüklenme süresi 1 yılı aştıysa güncellemeniz
                             için size bilgi gönderilecektir.""")
    title = forms.ChoiceField(required=True, choices=Profile.TITLE, label="Kurum bağlantınız:")
    phone = forms.CharField(widget=forms.TextInput, required=True, label="Telefon numaranız:")
    other_phone = forms.CharField(widget=forms.TextInput, required=False, label="Diğer telefon numaranız:")
    nationalid = forms.CharField(widget=forms.TextInput, required=False, label="T.C Kimlik Numaranız:")

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
                raise forms.ValidationError("Hata! 5xxxxxxxxx formatında giriniz.")
        except ValueError:
            raise forms.ValidationError("Bir telefon numarası giriniz.")
        return phone_number


class PasswordChangeForm(forms.Form):
    user = None
    old_password = forms.CharField(min_length=6, required=True, label='Mevcut şifreniz:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(min_length=6, required=True, label='Yeni şifreniz:',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="En az 6 karakter.")
    new_password_confirm = forms.CharField(min_length=6, required=True, label='Yeni şifre onay:',
                                           widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')

        if new_password != new_password_confirm:
            self.add_error('new_password', "Şifreler eşleşmedi.")
            self.add_error('new_password_confirm', "Şifreler eşleşmedi.")

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')

        if not self.user.check_password(old_password):
            raise forms.ValidationError("Mevcut şifreniz yanlış.")

        return old_password


class ForgotPasswordForm(forms.Form):
    nationalid = forms.IntegerField(required=False, label="T.C Kimlik Numaranız:")

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    def clean(self):
        nationalid = self.cleaned_data.get('nationalid', '')
        users = User.objects.all()
        if not str(nationalid) in users.values_list('profile__nationalid', flat=True):
            self.add_error('nationalid', 'Bu T.C Kimlik numarasına ilişkin hesap bulunamadı.')

        try:
            int(nationalid)
        except TypeError:
            self.add_error('nationalid', 'Geçersiz T.C Kimlik numarası.')
