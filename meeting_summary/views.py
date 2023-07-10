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
            summary = {
                "title": "Engineering Key Review Meeting Summary",
                "bullets": [
                    "Eric Johnson proposed breaking up the meeting into four department key reviews: development, quality, security and UX",
                    "The proposal suggests a two-month rotation for each department to avoid adding too many meetings to stakeholders' calendars",
                    "Discussion about R&D overall MR rate and R&D wider MR rate, including the need to clarify the definition and metrics",
                    "Consideration of measuring the percentage of total MRs that come from the community as a KPI",
                    "Concerns raised about the spike in meantime to close for S2 issues and the need for further investigation",
                    "Updates on defect tracking and SLO achievement metrics, including plans to measure the age of open bugs",
                    "Attention drawn to the decline in Sus score, but with improvements noted in the latest quarter",
                    "Discussion on the narrow MR rate, taking into account vacation days and expectations for a rebound in the following months",
                    "Importance of balancing productivity with other indicators related to quality, security, and availability"
                ]
            }

            # Save summary object to database if needed
            # summary_object = Summary(meeting_id=meeting_id, summary=summary)
            # summary_object.save()

            return JsonResponse({'meeting_id': meeting_id, 'summary': summary})

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
        "avatar": "https://images.unsplash.com/photo-1524666041070-9d87656c25bb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bWFsZXxlbnwwfHwwfHx8MA%3D%3D&w=1000&q=80",
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
        "avatar": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
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
        "avatar": "https://media.istockphoto.com/id/1317783028/photo/side-view-silhouette-of-business-man-isolate-on-white.jpg?s=612x612&w=0&k=20&c=gTU9UsKfxQ9m_RcrHl-iaAGUhsg-GPgQJ867u8zYc7w=",
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
        "avatar": "https://media.istockphoto.com/id/1504194952/photo/pretty-smiling-joyfully-female-dressed-casually-smiling-looking-with-satisfaction-at-camera.webp?b=1&s=170667a&w=0&k=20&c=Ll31aFaWj2omz-4wqxrsOWXwLJ5XfZEm8YUehHEbWGU=",
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

@csrf_exempt
def actionOwner(request):
    if request.method == 'GET':
        try:
            # Assuming that you have a function to fetch meeting labels
            #meeting_labels = meeting_key_labels(meeting_id)
            
            # get the user's audio breakpoints
            #audio_breakpoints_data = audio_breakpoints(meeting_id)

            actionOwner_data = [
    {
        "owner_id": 1,
        "name": "Eric Johnson"
    },
    {
        "owner_id": 2,
        "name": "Steve"
    },
    {
        "owner_id": 3,
        "name": "Christopher"
    },
     {
        "owner_id": 4,
        "name": "Dayne John"
    },
    {
        "owner_id": 4,
        "name": "Lyra"
    },
]

                
            response_data = {
                 actionOwner_data
            }

            return JsonResponse(response_data)

        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


