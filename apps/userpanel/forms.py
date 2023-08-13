from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from apps.accounts.models import User


class EditProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری', 'aria-describedby': 'username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': 'email-address'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    image_name = forms.CharField(widget=forms.HiddenInput())


class WalletChargeForm(forms.Form):
    amount = forms.IntegerField(error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'مبلغ به تومان', 'aria-describedby': 'amount'}))
