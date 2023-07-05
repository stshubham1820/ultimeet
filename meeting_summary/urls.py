from django.urls import path
from meeting_summary import views

urlpatterns = [
   path('meeting/<int:meeting_id>/summary_view/', views.summary_view, name='summary_view'),
   path('meeting/<int:meeting_id>/agenda/', views.agenda, name='agenda'),
   path('meeting/<int:meeting_id>/key_points/', views.key_points, name='key_points'),
   path('meeting/<int:meeting_id>/users_audio_breakpoints/', views.users_audio_breakpoints, name='users_audio_breakpoints'),
]

