from django.shortcuts import render

# Create your views here.
# importing libraries, functions and models
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Participant
from .engagement import engagement_levels

@csrf_exempt
def engagement(request, meeting_id):
    if request.method == 'GET':
        try:
            speaker_percentages, avg_speaker_percentage = engagement_levels(meeting_id)  
            # Include meeting_id and average speaker percentage in the response
            return JsonResponse({'meeting_id': meeting_id, 'Engagement': speaker_percentages, 'Average speaker percentage': avg_speaker_percentage})

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)





