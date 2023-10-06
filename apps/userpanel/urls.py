from django.urls import path
from .views import *

app_name = 'userpanel'
urlpatterns = [
    path('userpanel/', UserPanelInformationView.as_view(), name='UserPanelInformation'),
    path('editprofile/', EditProfileView.as_view(), name='EditProfile'),
    path('wallet/', WalletView.as_view(), name='Wallet'),
    path('master_panel/', MasterCoursesList.as_view(), name='MasterCoursesList'),
    path('master_episodes/<int:course_id>', MasterEpisodeList.as_view(), name='MasterEpisodeList'),
    path('add_episodes/<int:course_id>', AddEpisode.as_view(), name='AddEpisode'),
    path('dropzone_target/<int:course_id>', DropzoneTarget.as_view(), name='DropzoneTarget'),
]
