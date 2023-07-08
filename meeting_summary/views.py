# importing libraries, functions and models
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Participant
from meeting_summary.models import Summary
from .key_points import get_key_points
from .users_audio_breakpoints import audio_breakpoints, meeting_key_labels
from .agenda import meeting_agenda
from .summary_view import summary_text

@csrf_exempt
def summary_view(request, meeting_id):
    if request.method == 'GET':
        try:
            #meeting = Meeting.objects.get(id=meeting_id)
            summary = "At the meeting, the team discussed the productivity rate, which had been raised to eleven but was then brought back down to ten. It was decided that the productivity rate should be held at ten going forward, and that the team should focus on other indicators such as quality, security, and availability to improve. Eric Johnson then concluded the meeting and everyone said their goodbyes." #summary_text(meeting_id)
            #summary_object = Summary(meeting_id=meeting_id, summary=summary)
            #print('Summary:',summary_object)
            #summary_object.save()
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
            #audio_breakpoints_data = audio_breakpoints(meeting_id)

            audio_breakpoints_data = [
    {
        "name": "Eric Johnson",
        "avatar": "https://photos.com",
        "username": "ericjohnson",
        "audio_breakpoints": {
            "start": [
                8930,
                319630,
                324752,
                353740,
                921920,
                1197720
            ],
            "end": [
                176780,
                324714,
                331840,
                899080,
                1132960,
                1461650
            ]
        },
        "talk_time": 83.95
    },
    {
        "name": "B",
        "avatar": "https://photos.com",
        "username": "b",
        "audio_breakpoints": {
            "start": [
                177390
            ],
            "end": [
                185818
            ]
        },
        "talk_time": 0.59
    },
    {
        "name": "Dayne John",
        "avatar": "https://photos.com",
        "username": "daynejohn",
        "audio_breakpoints": {
            "start": [
                185914,
                901500
            ],
            "end": [
                318470,
                920380
            ]
        },
        "talk_time": 10.59
    },
    {
        "name": "Lyra",
        "avatar": "https://photos.com",
        "username": "lyra",
        "audio_breakpoints": {
            "start": [
                332450,
                1135650
            ],
            "end": [
                345570,
                1192180
            ]
        },
        "talk_time": 4.87
    }
]

                
            response_data = {
                'meeting_id': meeting_id,
                'mediaURL' : '/Users/sparshbohra/ultimeet/ultimeet_backend/ultimeet/recording_transcription/Panel_Discussion_AI.mp3',
                'meeting_key_labels': [meeting_labels],
                'users_audio_breakpoints': audio_breakpoints_data
            }

            return JsonResponse(response_data)

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


