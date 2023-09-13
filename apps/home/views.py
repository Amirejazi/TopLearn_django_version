from django.conf import settings
from django.db.models import Sum
from django.shortcuts import render
from django.views import View

from apps.course.models import Course


def media_admin(request):
    return {'media_url': settings.MEDIA_URL}


class Index(View):
    def get(self, request):
        latest_courses = Course.objects.order_by('createDate').annotate(total_time=Sum('episodes__episodeTime'))[:8]
        return render(request, 'Home_app/index.html', {'latest_courses': latest_courses})
