from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='Register'),
    path('activeCode/<str:activecode>', ActiveCode.as_view(), name='ActiveCode'),
    path('login/', LoginUserView.as_view(), name='Login'),
    path('logout/', LogoutUserView.as_view(), name='Logout'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='ForgotPassword'),
    path('resetpassword/<str:activecode>', ResetPasswordView.as_view(), name='ResetPassword'),
]
