from django.conf import settings
from django.shortcuts import render
from django.views import View


def media_admin(request):
    return {'media_url': settings.MEDIA_URL}


class Index(View):
    def get(self, request):
        return render(request, 'Home_app/index.html')
