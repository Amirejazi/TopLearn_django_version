from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserRegisterForm, UserLoginForm, ForgotPasswordForm, ResetPasswordForm
from uuid import uuid4
from .models import User
from django.http import HttpResponseNotFound
from .utils import SendEmail, ActivateCode


class RegisterUserView(View):
    template_name = 'Account_app/RegisterUser.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'خطا در انجام ثبت نام', 'danger')
            return render(request, self.template_name, {'form': form})
        data = form.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            active_code=str(uuid4()).replace('-', '')
        )

        SendEmail('Account_app/EmailTemplates/ActiveEmail.html', user, 'فعالسازی')

        return render(request, 'Account_app/SuccessRegister.html', {'user': user})


class ActiveCode(View):
    def get(self, request, *args, **kwargs):
        activeCode = kwargs['activecode']
        return render(request, 'Account_app/ActiveCode.html', {'IsActive': ActivateCode(activeCode)})


class LoginUserView(View):
    template_name = 'Account_app/Login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = UserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST)

        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})

        data = form.cleaned_data
        user = authenticate(request, username=data['email'], password=data['password'])

        if user is None:
            messages.error(request, "اطلاعات وارد شده نادرست میباشد!", 'danger')
            return render(request, self.template_name, {'form': form})

        user_db = User.objects.get(email=data['email'])

        if user_db.is_admin:
            messages.error(request, 'کاربر ادمین نمیتواند از اینجا وارد شود!', 'warning')
            return render(request, self.template_name, {'form': form})

        if user_db.is_active == False:
            messages.error(request, 'حساب کاربری شما فعال نمی باشد!', 'danger')
            return render(request, self.template_name, {'form': form})

        login(request, user)
        next_url = request.GET.get('next')
        if next_url is not None:
            context = {
                'form': form,
                'IsSuccess': True,
                'next_url': next_url
            }
            return render(request, self.template_name, context)
        else:
            context = {
                'form': form,
                'IsSuccess': True
            }
            return render(request, self.template_name, context)


class LogoutUserView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:index')


class ForgotPasswordView(View):
    template_name = 'Account_app/ForgotPassword.html'

    def get(self, request, *args, **kwargs):
        form = ForgotPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ForgotPasswordForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})
        try:
            data = form.cleaned_data
            user = User.objects.get(email=data['email'])
            SendEmail('Account_app/EmailTemplates/ForgotPasswordEmail.html', user, ' بازیابی رمز عبور')
            context = {
                'form': form,
                'IsSuccess': True
            }
            return render(request, self.template_name, context)
        except User.DoesNotExist:
            form.add_error('email', 'کاربری با این ایمیل یافت نشد!')
            return render(request, self.template_name, {'form': form})


class ResetPasswordView(View):
    template_name = 'Account_app/ResetPassword.html'

    def get(self, request, *args, **kwargs):
        initial_dict = {
            'active_code': kwargs['activecode']
        }
        form = ResetPasswordForm(initial=initial_dict)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ResetPasswordForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})
        try:
            data = form.cleaned_data
            user = User.objects.get(active_code=data['active_code'])
            user.set_password(data['password'])
            user.save()
            context = {
                'form': form,
                'IsSuccess': True
            }
            return render(request, self.template_name, context)
        except User.DoesNotExist:
            return HttpResponseNotFound()
