from django.urls import path
from .views import *

app_name = 'userpanel'
urlpatterns = [
    path('userpanel/', UserPanelInformationView.as_view(), name='UserPanelInformation'),
    path('editprofile/', EditProfileView.as_view(), name='EditProfile'),
    path('wallet/', WalletView.as_view(), name='Wallet'),
]
