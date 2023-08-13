from django.urls import path
from .views import *

app_name = 'payments'
urlpatterns = [
    path('charge_request/<int:wallet_id>', PaymentForChargeWalletRequestView.as_view(), name='ChargeWalletRequest'),
    path('charge_verify/', ZarinPalPaymentVerifyView.as_view(), name='VerifyPayment'),
    path('verifymessage/', ShowVerifyMessage, name='VerifyMessage'),
]
