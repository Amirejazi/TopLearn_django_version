import json
from django.conf import settings
from django.db.models import Sum
from django.http import HttpResponseNotFound, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from apps.course.models import Course


def media_admin(request):
    return {'media_url': settings.MEDIA_URL}


class Index(View):
    def get(self, request):
        return render(request, 'Home_app/index.html')


class Error404(TemplateView):
    template_name = "Home_app/Error404.html"


def latest_course(request):
    latest_courses = Course.objects.order_by('-createDate').annotate(total_time=Sum('episodes__episodeTime'))[:8]
    return render(request, 'Course_app/render_partials/LatestCourse.html', {'latest_courses': latest_courses})


def popular_courses(request):
    popular_course = Course.objects.annotate(order_detail_count=Sum('order_details__count')) \
                         .order_by('-order_detail_count') \
                         .annotate(total_time=Sum('episodes__episodeTime'))[:8]
    return render(request, 'Course_app/render_partials/PopularCourse.html', {'popular_courses': popular_course})


def search_complete(request):
    term = request.GET.get('term')
    if term is not None:
        # چون میخواهیم خروجیمان بصورت لیست باشد falt را true میگذاریم
        course_titles = Course.objects.filter(courseTitle__icontains=term).values_list('courseTitle', flat=True)
        return HttpResponse(json.dumps(list(course_titles), ensure_ascii=False), content_type="application/json")
    return HttpResponseNotFound()
