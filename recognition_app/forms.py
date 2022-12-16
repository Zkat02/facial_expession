from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from .models import Profile,User
from .models import Calculation, Profile
from django.forms import TextInput
import logging

logger = logging.getLogger(__name__)


class CalculationForm(forms.ModelForm):
    class Meta:
        model = Calculation
        fields = ['calculation_name', 'calculation_image', 'info']
        widgets = {
            "calculation_name": forms.TextInput(attrs={"class": "form-control"}),
            "info": forms.Textarea(attrs={"class": "form-control", 'cols': 10, "rows": 3}),
            "calculation_image": forms.FileInput(attrs={"class": "form-control"})
        }
        labels = {
            'calculation_name': 'Name of calculation'
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date','photo','amount_calculations']
        widgets = {
            "bio": forms.Textarea(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control", 'cols': 10, "rows": 3}),
            "birth_date": forms. DateInput(attrs={"class": "form-control"}),
            'photo':  forms.FileInput(attrs={"class": "form-control"}),
            'amount_calculations': forms.TextInput(attrs={"readonly": "readonly","class": "form-control"}),
        }


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
