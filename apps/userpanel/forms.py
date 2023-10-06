from django import forms


class EditProfileForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'نام کاربری', 'aria-describedby': 'username'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'ایمیل', 'aria-describedby': 'email-address'}))
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    image_name = forms.CharField(widget=forms.HiddenInput())


class WalletChargeForm(forms.Form):
    amount = forms.IntegerField(error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                widget=forms.NumberInput(
                                    attrs={'class': 'form-control', 'min': '0', 'placeholder': 'مبلغ به تومان', 'aria-describedby': 'amount'}))


class AddEpisodeForm(forms.Form):
    course_id = forms.CharField(required=True, widget=forms.HiddenInput())
    title = forms.CharField(required=True, error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان'}))
    episodefilename = forms.CharField(required=True, error_messages={'required': 'این فیلد نمی تواند خالی باشد!'}, widget=forms.HiddenInput())
    episodeTime = forms.DurationField(required=True, error_messages={'required': 'این فیلد نمی تواند خالی باشد!'},
                                  widget=forms.TimeInput(attrs={'class': 'form-control', 'placeholder': '00:00:00'}))
    is_free = forms.BooleanField(required=False, widget=forms.CheckboxInput())
