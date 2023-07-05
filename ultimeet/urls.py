
#from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('user_authentication/', include('user_authentication.urls')),
    path('recording_transcription/', include('recording_transcription.urls')),
    path('meeting_summary/', include('meeting_summary.urls')),
    path('meeting_action_tasks/', include('meeting_action_tasks.urls')),
    path('analytics/', include('analytics.urls')),

   # path('', views.home, name='home'),
    #path('start_recording/', views.start_recording, name='start_recording'),
    #path('stop_recording/', views.stop_recording, name='stop_recording'),
    #path('process_speech/', views.process_speech, name='process_speech'),

]


