import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Q, Sum, Min, Max
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseNotFound
from TopLearn import settings
from .models import CourseGroup, Course, Episode, CourseComment, CourseVote
from .utils import apply_filters_on_courses, add_order, downloadFile


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

        course_per_page = 3
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


class ShowCourse(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # برای استفاده از متد annotate ابتدا مجبور به استفاده از filter سپس get شدیم
            course = Course.objects.filter(id=kwargs['id']).annotate(total_time=Sum('episodes__episodeTime'))
            course = course.get(id=kwargs['id'])
            tags = course.tags.split('-')
            is_user_in_course = False
            if user.is_authenticated:
                is_user_in_course = user.is_user_in_course(course.id)

            ep = None
            active_demo = True
            episode = request.GET.get('episode')
            if not episode is None and user.is_authenticated:
                if not course.episodes.filter(id=episode).exists():
                    return HttpResponseNotFound()
                if not course.episodes.get(id=episode).is_free:
                    if not user.is_user_in_course(course.id):
                        return HttpResponseNotFound()
                ep = course.episodes.get(id=episode)
                active_demo = False


            context = {
                'course': course,
                'tags': tags,
                'is_user_in_course': is_user_in_course,
                'ep': ep,
                'active_demo': active_demo
            }
            return render(request, 'Course_app/ShowCourse.html', context)
        except Course.DoesNotExist:
            return HttpResponseNotFound()


class BuyCourse(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            course = Course.objects.get(id=kwargs['course_id'])
            order_id = add_order(user, course)
            return redirect(f'/order/show_order/{order_id}')
        except Course.DoesNotExist:
            return HttpResponseNotFound()


class DownloadFiles(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            episode = Episode.objects.get(id=kwargs['episode_id'])
            file_path = os.path.join(settings.MEDIA_ROOT, str(episode.episodefilename))
            if episode.is_free:
                return downloadFile(file_path)
            if user.is_authenticated:
                if user.is_user_in_course(episode.course.id):
                    return downloadFile(file_path)
            return HttpResponseForbidden()
        except Episode.DoesNotExist:
            return HttpResponseNotFound()


class CreateComment(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.POST.get('comment_course_id')
        CourseComment.objects.create(
            course_id=course_id,
            user=user,
            comment=request.POST.get('comment_text'),
        )
        return redirect(f'/course/show_comments/{course_id}')


def show_comments(request, course_id):
    comments = CourseComment.objects.filter(course__id=course_id)
    if comments.count() > 5:
        comments_per_page = 5
        paginator = Paginator(comments, comments_per_page)
        page_number = request.GET.get('pageId')
        page_obj = paginator.get_page(page_number)
    else:
        page_obj = comments
    return render(request, 'Course_app/ShowComments.html', {'page_obj': page_obj})


class ShowCourseVote(View):
    def get(self, request, course_id):
        user = request.user
        is_show_likes = False
        course = Course.objects.get(id=course_id)

        if course.price != 0:
            if user.is_authenticated and user.is_user_in_course(course_id):
                is_show_likes = True
        like_count = CourseVote.objects.filter(Q(vote=True) & Q(course_id=course_id)).count()
        dislike_count = CourseVote.objects.filter(Q(vote=False) & Q(course_id=course_id)).count()
        context = {
            'like_count': like_count,
            'dislike_count': dislike_count,
            'is_show_likes': is_show_likes
        }
        return render(request, 'Course_app/ShowVotes.html', context)


@login_required
def add_vote(request, course_id):
    user = request.user
    vote = request.GET.get('vote')
    try:
        user_vote = CourseVote.objects.get(Q(user=user) & Q(course_id=course_id))
        user_vote.vote = vote
        user_vote.save()
    except CourseVote.DoesNotExist:
        CourseVote.objects.create(user=user, course_id=course_id, vote=vote)
    return redirect(f'/course/show_votes/{course_id}')
