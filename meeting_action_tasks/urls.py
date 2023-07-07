from django.urls import path
from meeting_action_tasks import views

urlpatterns = [
   #path('action_items/', views.action_items, name='action_items'),
   path('generate_action_items/<int:meeting_id>/', views.generate_action_items, name='generate_action_items'),
   path('get_action_items_by_meeting_id/<int:meeting_id>/', views.get_action_items_by_meeting_id, name='get_action_items_by_meeting_id'),
   path('get_action_item_by_id/<int:action_item_id>/', views.get_action_item_by_id, name='get_action_item_by_id'),
   path('update_action_item/<int:action_item_id>/', views.update_action_item, name='update_action_item'),
   
]
