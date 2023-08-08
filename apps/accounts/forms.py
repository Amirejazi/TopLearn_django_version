from django import forms
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError



class UserRegisterForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری', 'aria-describedby': 'username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': 'email-address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور', 'aria-describedby': 'password'}))
    rePassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور', 'aria-describedby': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['username'].error_messages.update({
            'unique': 'این نام کاربری قبلا استفاده شده است!',
        })

        self.fields['email'].error_messages.update({
            'unique': 'این ایمیل قبلا استفاده شده است!',
        })

    def clean_rePassword(self):
        pass1 = self.cleaned_data["password"]
        pass2 = self.cleaned_data["rePassword"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return pass2


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': "email-address"}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور', 'aria-describedby': "email-address" }))
    remember_me = forms.BooleanField()
