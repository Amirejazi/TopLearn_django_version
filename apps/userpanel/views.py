from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.userpanel.forms import EditProfileForm, WalletChargeForm
from apps.userpanel.models import Wallet, WalletType


class UserPanelInformationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "userPanel_app/UserPanelinfo.html")


class EditProfileView(LoginRequiredMixin, View):
    template_name = "userPanel_app/EditProfile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        initial_dict = {
            'email': user.email,
            'username': user.username,
            'image_name': user.image_name
        }
        form = EditProfileForm(initial=initial_dict)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})
        data = form.cleaned_data
        user = request.user
        try:
            user.email = data['email']
            user.save()
        except:
            form.add_error('email', 'این ایمیل قبلا استفاده شده است!')
            return render(request, self.template_name, {'form': form})
        try:
            user.username = data['username']
            user.save()
        except:
            form.add_error('username', 'این نام کاربری قبلا استفاده شده است!')
            return render(request, self.template_name, {'form': form})
        if data['image'] is not None:
            user.image_name = data['image']
        user.save()
        logout(request)
        return redirect("/account/login?EditProfile=true")


class WalletView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = WalletChargeForm()
        context = {
            'form': form,
        }
        return render(request, "UserPanel_app/Wallet.html", context)

    def post(self, request, *args, **kwargs):
        form = WalletChargeForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, "UserPanel_app/Wallet.html", {'form': form})
        user = request.user
        data = form.cleaned_data
        wallet = Wallet.objects.create(
            type=get_object_or_404(WalletType, type_id=1),
            user=user,
            amount=data['amount'],
            description='شارژ حساب'
        )
        return redirect('payment:ChargeWalletRequest', wallet.id)
