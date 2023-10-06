import os
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from TopLearn.settings import MEDIA_ROOT
from apps.course.models import Course, Episode
from apps.userpanel.forms import EditProfileForm, WalletChargeForm, AddEpisodeForm
from apps.userpanel.models import Wallet, WalletType


class UserPanelInformationView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "userPanel_app/UserPanelinfo.html")


class EditProfileView(LoginRequiredMixin, View):
    template_name = "userPanel_app/EditProfile.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        initial_dict = {
            'email': user.email,
            'username': user.username,
            'image_name': user.image_name
        }
        form = EditProfileForm(initial=initial_dict)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = EditProfileForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, self.template_name, {'form': form})
        data = form.cleaned_data
        user = request.user
        try:
            user.email = data['email']
            user.save()
        except:
            form.add_error('email', 'این ایمیل قبلا استفاده شده است!')
            return render(request, self.template_name, {'form': form})
        try:
            user.username = data['username']
            user.save()
        except:
            form.add_error('username', 'این نام کاربری قبلا استفاده شده است!')
            return render(request, self.template_name, {'form': form})
        if data['image'] is not None:
            user.image_name = data['image']
        user.save()
        logout(request)
        return redirect("/account/login?EditProfile=true")


class WalletView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = WalletChargeForm()
        context = {
            'form': form,
        }
        return render(request, "UserPanel_app/Wallet.html", context)

    def post(self, request, *args, **kwargs):
        form = WalletChargeForm(request.POST)
        if not form.is_valid():
            messages.error(request, 'اطلاعات وارد شده نا معتبر می باشد!', 'danger')
            return render(request, "UserPanel_app/Wallet.html", {'form': form})
        user = request.user
        data = form.cleaned_data
        wallet = Wallet.objects.create(
            type=get_object_or_404(WalletType, type_id=1),
            user=user,
            amount=data['amount'],
            description='شارژ حساب'
        )
        return redirect('payment:ChargeWalletRequest', wallet.id)


class MasterCoursesList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'course.master_panel'

    def get(self, request, *args, **kwargs):
        user = request.user
        courses = Course.objects.filter(teacher_id=user.id)
        return render(request, 'UserPanel_app/MasterCoursesList.html', {'courses': courses})


class MasterEpisodeList(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'course.master_panel'

    def get(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs['course_id']
        try:
            course = Course.objects.get(id=course_id)
            if course.teacher_id != user.id:
                return redirect('userpanel:MasterCoursesList')
            return render(request, 'UserPanel_app/EpisodeList.html', {'course': course})
        except Course.DoesNotExist:
            return HttpResponseNotFound()


class AddEpisode(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'course.master_panel'

    def get(self, request, *args, **kwargs):
        user = request.user
        course_id = kwargs.get('course_id')
        try:
            course = Course.objects.get(id=course_id)
            if course.teacher_id != user.id:
                return redirect('userpanel:MasterCoursesList')
            form = AddEpisodeForm(initial={'course_id': course.id})
            return render(request, 'UserPanel_app/AddEpisode.html', {'form': form})
        except Course.DoesNotExist:
            return HttpResponseNotFound()

    def post(self, request, *args, **kwargs):
        form = AddEpisodeForm(request.POST)
        if not form.is_valid():
            return render(request, 'UserPanel_app/AddEpisode.html', {'form': form})
        data = form.cleaned_data
        Episode.objects.create(
            episodeTitle=data['title'],
            course_id=data['course_id'],
            episodeTime=data['episodeTime'],
            is_free=data['is_free'],
            episodefilename=data['episodefilename']
        )
        return redirect('userpanel:MasterEpisodeList', course_id=data['course_id'])


class DropzoneTarget(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        course_id = kwargs.get('course_id')
        if not files is None:
            for file in files:
                file_name = f"{course_id}-{uuid4()}" + os.path.splitext(file.name)[-1]
                path = os.path.join(MEDIA_ROOT, 'coursefiles')
                if not os.path.exists(path):
                    os.makedirs(path)
                fs = FileSystemStorage(location=path)
                fs.save(file_name, file)
                return JsonResponse({'data': ('coursefiles/'+file_name), 'status': 'Success'})
        else:
            return JsonResponse({'status': 'Error'})
