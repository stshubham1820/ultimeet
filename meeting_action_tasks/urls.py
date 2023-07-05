from django.urls import path
from meeting_action_tasks import views

urlpatterns = [
   path('action_items/', views.action_items, name='action_items'),
   
]
