import re


class SecurityOfMediaMiddleware:
    def __init__(self, get_response):
        self.pattern = re.compile(r'^/+media/+coursefiles(/.*)?$')
        self.get_response = get_response

    def __call__(self, request):
        if self.pattern.match(request.path.lower()):
            referer_url = request.META.get('HTTP_REFERER', '')

            if referer_url != '' and (referer_url.startswith('https://127.0.0.1:8000/') or referer_url.startswith('http://127.0.0.1:8000/')):
                pass  # به درخواست بعدی ادامه دهد
            else:
                # تغییر آدرس، به URL ورود
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect('/account/login')

        response = self.get_response(request)
        return response
