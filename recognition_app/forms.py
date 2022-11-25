from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from .models import Profile,User
from .models import Calculation


# class AnaliseImageForm(forms.Form):
#     photo = forms.ImageField()
#     info = forms.CharField(label="Additional Info", required=False, widget=forms.Textarea(attrs={"class": "form-control", "rows": 5}))
#
#     def clean_photo(self):
#         photo = self.cleaned_data['photo']
#         if photo.size != (48,48):
#              photo = photo.resize((48, 48))
#         return photo


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ['title', 'calculation_image', 'info']
        exclude = ('user',)
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CalculationForm, self).__init__(*args, **kwargs)


#
# class CalculationForm(forms.ModelForm):
#     class Meta:
#         model = Calculation
#         fields = ['title','calculation_image', 'info'] #'user',
#         # widgets = {'user': forms.HiddenInput()}


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))
    content = forms.CharField(label="Текст", required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": 5}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))
    password = forms.CharField(label='пароль', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={"class": "form-control"}
    ))
    email = forms.CharField(label='email', widget=forms.EmailInput(
        attrs={"class": "form-control"}))
    password1 = forms.CharField(label='пароль', help_text='пароль должен содержать не менее 8ми символов',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control"}))
    password2 = forms.CharField(label='подтвержение пароля', widget=forms.PasswordInput(
        attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = {'username', 'email', 'password1', 'password2'}


