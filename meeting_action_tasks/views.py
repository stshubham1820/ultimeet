from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .action_items import get_action_items

@csrf_exempt
def action_items(request):
    if request.method == 'POST':
            get_actions = get_action_items(request)
            return JsonResponse({'Action Items': get_actions})
            
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)