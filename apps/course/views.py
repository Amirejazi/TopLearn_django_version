from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Q, Sum, Min, Max
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View

from .models import CourseGroup, Course
from .utils import apply_filters_on_courses


def CourseGroupMenu(request):
    groups = CourseGroup.objects.filter(Q(parent=None) & Q(is_active=True))
    return render(request, 'Course_app/render_partials/CourseGroupMenu.html', {'groups': groups})


def GetSubGroupsJson(request, id):
    subgroups = CourseGroup.objects.filter(Q(parent__id=id) & Q(is_active=True))
    data = serialize("json", subgroups, fields=('groupTitle',))
    return HttpResponse(data, content_type="application/json")


class CourseList(View):
    def get(self, request, *args, **kwargs):
        main_groups = CourseGroup.objects.filter(Q(parent=None) & Q(is_active=True))
        courses = Course.objects.order_by('-createDate').annotate(total_time=Sum('episodes__episodeTime'))
        res_aggre = courses.aggregate(min=Min('price'), max=Max('price'))

        search_filter = request.GET.get('filter')
        get_type = request.GET.get('getType')
        order_by_type = request.GET.get('orderByType')
        start_price = request.GET.get('startPrice')
        end_price = request.GET.get('endPrice')
        group_filter = request.GET.getlist('selectedGroup')

        courses = apply_filters_on_courses(courses, search_filter, get_type, order_by_type, start_price, end_price, group_filter)

        course_per_page = 1
        paginator = Paginator(courses, course_per_page)
        page_number = request.GET.get('pageId')
        page_obj = paginator.get_page(page_number)
        courses_count = courses.count()

        context = {
            "main_groups": main_groups,
            "res_aggre": res_aggre,
            "page_obj": page_obj,
            "courses_count": courses_count,
            "page_number": page_number,
        }
        return render(request, 'Course_app/CourseList.html', context)
