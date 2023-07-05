from django.urls import path
from analytics import views

urlpatterns = [
   path('meeting/<int:meeting_id>/engagement/', views.engagement, name='engagement'),
]

