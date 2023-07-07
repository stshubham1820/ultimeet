from django.urls import path
from recording_transcription import views

urlpatterns = [
   path('create_meeting/', views.create_meeting, name='create_meeting'),
   path('get_meeting/<int:meeting_id>/', views.get_meeting, name='get_meeting'),
   path('transcription_view/<int:meeting_id>/', views.transcription_view, name='transcription_view'),
   path('create_transcript/<int:meeting_id>/', views.create_transcript, name='create_transcript'),
   path('get_participant_list/<int:meeting_id>/', views.get_participant_list, name='get_participant_list'),
   # path('meeting/<int:meeting_id>/create_transcript/', views.create_transcript, name='create_transcript'),
   path('get_transcription/<int:meeting_id>/', views.get_transcription, name='get_transcription'),
   path('start-recording/<int:meeting_id>/', views.start_recording, name='start-recording'),
   path('stop-recording/<int:meeting_id>/', views.stop_recording, name='stop-recording'),
   path('priorities/', views.priority_list, name='priority-list'),
   path('status/', views.status_list, name='status-list'),
]
