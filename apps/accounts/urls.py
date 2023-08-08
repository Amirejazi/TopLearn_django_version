from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='Register'),
    path('successRegister/', SuccessRegister.as_view(), name='SuccessRegister'),
    path('activeCode/<str:activecode>', ActiveCode.as_view(), name='ActiveCode'),
    path('login/', LoginUserView.as_view(), name='Login'),
    path('logout/', LogoutUserView.as_view(), name='Logout'),
]
