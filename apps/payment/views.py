from django.conf import settings
import requests
import json

# ? sandbox merchant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from apps.userpanel.models import Wallet

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

MERCHANT = "00000000-0000-0000-0000-000000000000"
CallbackURL = 'http://127.0.0.1:8000/payment/charge_verify/'


class PaymentForChargeWalletRequestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(id=kwargs['wallet_id'])
            data = {
                "MerchantID": MERCHANT,
                "Amount": wallet.amount,
                "Description": wallet.description,
                "CallbackURL": CallbackURL,
            }
            request.session['payment_session'] = {
                'wallet_id': wallet.id,
            }
            data = json.dumps(data)
            # set content length by data
            headers = {'content-type': 'application/json', 'content-length': str(len(data))}
            try:
                response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response['Status'] == 100:
                        return redirect(ZP_API_STARTPAY + str(response['Authority']))
                    else:
                        return JsonResponse({'status': False, 'code': str(response['Status'])})
                return JsonResponse(response)

            except requests.exceptions.Timeout:
                return JsonResponse({'status': False, 'code': 'timeout'})
            except requests.exceptions.ConnectionError:
                return JsonResponse({'status': False, 'code': 'connection error'})
        except Wallet.DoesNotExist:
            return redirect('userpanel:Wallet')


class ZarinPalPaymentVerifyView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        authority = request.GET.get('Authority')
        wallet_id = request.session['payment_session']['wallet_id']
        wallet = Wallet.objects.get(id=wallet_id)
        data = {
            "MerchantID": MERCHANT,
            "Amount": wallet.amount,
            "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                wallet.is_pay = True
                wallet.save()
                return redirect(f"/payment/verifymessage?RefID={response['RefID']}")
            else:
                return redirect('/payment/verifymessage')
        return response


def ShowVerifyMessage(request):
    return render(request, 'UserPanel_app/VerifyMessage.html', {'RefID': request.GET.get('RefID')})
