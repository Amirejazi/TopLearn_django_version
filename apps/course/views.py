from django.core.serializers import serialize
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from .models import CourseGroup


def CourseGroupMenu(request):
    groups = CourseGroup.objects.filter(Q(parent=None) & Q(is_active=True))
    return render(request, 'Course_app/render_partials/CourseGroupMenu.html', {'groups': groups})


def GetSubGroupsJson(request, id):
    subgroups = CourseGroup.objects.filter(Q(parent__id=id) & Q(is_active=True))
    data = serialize("json", subgroups, fields=('groupTitle',))
    return HttpResponse(data, content_type="application/json")
