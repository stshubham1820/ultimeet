# importing libraries, functions and models
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Participant
from .key_points import get_key_points
from .users_audio_breakpoints import audio_breakpoints, meeting_key_labels
from .agenda import meeting_agenda
from .summary_view import summary_text

@csrf_exempt
def summary_view(request, meeting_id):
    if request.method == 'GET':
        try:
            summary = summary_text(meeting_id)
            return JsonResponse({'meeting_id': meeting_id,'summary': summary})

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def agenda(request, meeting_id):
    if request.method == 'GET':
        try:
            agenda = meeting_agenda(meeting_id)
            return JsonResponse({'Agenda': agenda})

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def key_points(request, meeting_id):
    if request.method == 'GET':
        try:
            points = get_key_points(meeting_id)  
            return JsonResponse({'Key-Points': points})

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def users_audio_breakpoints(request, meeting_id):
    if request.method == 'GET':
        try:
            # Assuming that you have a function to fetch meeting labels
            meeting_labels = meeting_key_labels(meeting_id)
            
            # get the user's audio breakpoints
            audio_breakpoints_data = audio_breakpoints(meeting_id)
                
            response_data = {
                'meeting_id': meeting_id,
                'mediaURL' : '/Users/sparshbohra/ultimeet/ultimeet_backend/ultimeet/recording_transcription/Panel_Discussion_AI.mp3',
                'meeting_key_labels': [meeting_labels],
                'users_audio_breakpoints': audio_breakpoints_data['users_audio_breakpoints']
            }

            return JsonResponse(response_data)

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


