from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری', 'aria-describedby': 'username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': 'email-address'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور', 'aria-describedby': 'password'}))
    rePassword = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور', 'aria-describedby': 'password'}))

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
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': "email-address"}))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور', 'aria-describedby': "email-address"}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())


class ForgotPasswordForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': "email-address"}))

    class Meta:
        model = User
        fields = ['email']


class ResetPasswordForm(forms.Form):
    active_code = forms.CharField(widget=forms.HiddenInput())
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'رمز عبور', 'aria-describedby': 'password'}))
    rePassword = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور', 'aria-describedby': 'Repassword'}))


# =============================================================================================================


class UserCreationForm(forms.ModelForm):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password1 = forms.CharField(label='رمزعبور', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار رمزعبور', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'image_name')

    def clean_password2(self):
        pass1 = self.cleaned_data["password1"]
        pass2 = self.cleaned_data["password2"]
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('رمز عبور با تکرار آن مغایرت دارد!')
        return pass2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ======================================================================================
class UserChangeForm(forms.ModelForm):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}))
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل'}))
    password = ReadOnlyPasswordHashField(help_text="برای تغییر رمز عبور <a href='../password'> اینجا</a> کلیک کنید")

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')
