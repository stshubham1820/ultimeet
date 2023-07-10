from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Transcript, Priority,Status,meeting_user_details,Comments
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
import json
from datetime import datetime
from .transcript import process_transcription




from .models import Meeting, Participant, Absents, Action_Item_Approved_By,Transcript

@csrf_exempt
def get_meeting(request, meeting_id):
    if request.method == 'GET':
        try:
            # Retrieve the meeting object using the meeting_id
            meeting = Meeting.objects.get(pk=meeting_id)

            # Print meeting ID for debugging
            print(f"Meeting ID: {meeting.meeting_id}")

            # Retrieve related objects
            participants = Participant.objects.filter(meeting=meeting)
            #participants = meeting.participants_list.all()

            # Print the count of participants for debugging
            print(f"Participants count: {participants.count()}")

            # Create lists to store participant data
            participants_list = []

            # Retrieve participant data
            for participant in participants:
                participant_data = {
                    'name': participant.name,
                    'email': participant.email,
                    'profile_picture': participant.profile_picture,
                }
                participants_list.append(participant_data)

            # Convert the meeting object to a JSON response
            response_data = {
                'meeting_id': meeting.meeting_id,
                'meeting_title': meeting.meeting_title,
                'meeting_from': meeting.meeting_from.strftime('%Y-%m-%d %H:%M:%S'),
                'meeting_to': meeting.meeting_to.strftime('%Y-%m-%d %H:%M:%S'),
                'meeting_organizer': {
                    'email': meeting.meeting_organizer_email,
                    'username': meeting.meeting_organizer_username,
                },
                'meeting_type': meeting.meeting_type,
                'meeting_channel': meeting.meeting_channel,
                'meeting_nature': meeting.meeting_nature,
                'participants_list': participants_list,
                'meeting_description': meeting.meeting_description,
                'meeting_location': meeting.meeting_location,
                'meeting_action_items_count': meeting.meeting_action_items_count,
            }

            return JsonResponse(response_data, status=200)
        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)


@csrf_exempt
def get_participant_list(request, meeting_id):
    if request.method == 'GET':
        try:
            participants = Participant.objects.filter(meeting__pk=meeting_id)
            absents = Absents.objects.filter(meeting__pk=meeting_id)

            participants_list = []
            for participant in participants:
                participant_data = {
                    'name': participant.name,
                    'email': participant.email,
                    'profile_picture': participant.profile_picture,
                }
                participants_list.append(participant_data)

            return JsonResponse(participants_list, safe=False)
        except Participant.DoesNotExist:
            return JsonResponse({'error': 'Participants not found for the meeting.'})

@csrf_exempt
def get_action_item_approved_by_list(request, meeting_id):
    if request.method == 'GET':
        try:
            # Retrieve the participants list for the meeting using the meeting_id
            action_item_approved_bys = Action_Item_Approved_By.objects.filter(meeting__pk=meeting_id)

            absents = Action_Item_Approved_By.objects.filter(meeting__pk=meeting_id)

            

            # Create a list to store participant data
            action_item_approved_by_list = []

            # Iterate over the participants and retrieve their information
            for action_item_approved_by in action_item_approved_bys:
                action_item_approved_by_data = {
                    'name': action_item_approved_by.name,
                    'email': action_item_approved_by.email,
                    'profile_picture': action_item_approved_by.profile_picture,
                }
                action_item_approved_by_list.append(action_item_approved_by_data)

            # Return the participant list as a JSON response
            return action_item_approved_by_list
        except Participant.DoesNotExist:
            return 'action_item_approved_by not found for the meeting.'

@csrf_exempt
def get_absent_list(request, meeting_id):
    if request.method == 'GET':
        try:
            # Retrieve the participants list for the meeting using the meeting_id
            absents = Absents.objects.filter(meeting__pk=meeting_id)

            

            # Create a list to store participant data
            absents_list = []

            # Iterate over the participants and retrieve their information
            for absent in absents:
                absents_data = {
                    'name': absent.name,
                    'email': absent.email,
                    'profile_picture': absent.profile_picture,
                }
                absents_list.append(absents_data)

            # Return the participant list as a JSON response
            return absents_list
        except Absents.DoesNotExist:
            return 'Participants not found for the meeting.'

@csrf_exempt
def create_meeting(request):
    if request.method == 'POST':
        # Retrieve the JSON data from the request body
        data = json.loads(request.body)

        # Retrieve the data from the JSON object
        meeting_title = data.get('meeting_title')
        meeting_from = data.get('meeting_from')
        meeting_to = data.get('meeting_to')
        meeting_organizer = data.get('meeting_organizer')
        meeting_type = data.get('meeting_type')
        meeting_channel = data.get('meeting_channel')
        participants_list = data.get('participants_list')
        meeting_nature = data.get('meeting_nature')
        profile_picture = data.get('profile_picture')

        # Assuming meeting_organizer is an object with properties like 'id', 'email', 'username'
        # organizer_id = meeting_organizer.get('id')
        organizer_email = meeting_organizer.get('email')
        organizer_username = meeting_organizer.get('username')

        # Convert meeting_from and meeting_to to datetime objects
        from_date = datetime.strptime(meeting_from, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.strptime(meeting_to, '%Y-%m-%d %H:%M:%S')

        # Create a Picture object for the profile picture
        # picture = Picture(profile_picture=profile_picture)
        # picture.save()

        # Create a new Meeting object with the retrieved data
        meeting = Meeting(
            meeting_title=meeting_title,
            meeting_from=from_date,
            meeting_to=to_date,
            # meeting_organizer_id=organizer_id,
            meeting_organizer_email=organizer_email,
            meeting_organizer_username=organizer_username,
            meeting_type=meeting_type,
            meeting_channel=meeting_channel,
            meeting_nature=meeting_nature
            # profile_picture=picture
        )

        # Save the meeting object
        meeting.save()

        # Process the participants list if it is not None and not empty
from django.http import JsonResponse

@csrf_exempt
def create_meeting(request):
    if request.method == 'POST':
        # Retrieve the JSON data from the request body
        data = json.loads(request.body)

        # Retrieve the data from the JSON object
        meeting_title = data.get('meeting_title')
        meeting_from = data.get('meeting_from')
        meeting_to = data.get('meeting_to')
        meeting_organizer = data.get('meeting_organizer')
        meeting_type = data.get('meeting_type')
        meeting_channel = data.get('meeting_channel')
        participants_list = data.get('participants_list')
        meeting_nature = data.get('meeting_nature')
        profile_picture = data.get('profile_picture')

        # Assuming meeting_organizer is an object with properties like 'id', 'email', 'username'
        # organizer_id = meeting_organizer.get('id')
        organizer_email = meeting_organizer.get('email')
        organizer_username = meeting_organizer.get('username')

        # Convert meeting_from and meeting_to to datetime objects
        from_date = datetime.strptime(meeting_from, '%Y-%m-%d %H:%M:%S')
        to_date = datetime.strptime(meeting_to, '%Y-%m-%d %H:%M:%S')

        # Create a new Meeting object with the retrieved data
        meeting = Meeting(
            meeting_title=meeting_title,
            meeting_from=from_date,
            meeting_to=to_date,
            meeting_organizer_email=organizer_email,
            meeting_organizer_username=organizer_username,
            meeting_type=meeting_type,
            meeting_channel=meeting_channel,
            meeting_nature=meeting_nature
        )

        # Save the meeting object
        meeting.save()

        # Process the participants list if it is not None and not empty
        if participants_list is not None and len(participants_list) > 0:
            for participant_data in participants_list:
                participant_name = participant_data.get('name')
                participant_username = participant_data.get('username')
                participant_email = participant_data.get('email')
                participant_profile_picture = participant_data.get('profile_picture')

                participant = Participant(
                    meeting=meeting,
                    name=participant_name,
                    email=participant_email,
                    username=participant_username,
                    profile_picture=participant_profile_picture
                )
                participant.save()

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Meeting created successfully.'}, status=201)

    # Handle invalid request method (e.g., GET, PUT, DELETE)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)




@csrf_exempt
def get_transcription(request, meeting_id):
    if request.method == 'GET':
        print('API Called:',meeting_id)
        #meetingid=getMeeting_id(meeting_id)
        # Retrieve the JSON data from the request body
        data = json.loads(request.body)

        # Retrieve the data from the JSON object
        raw_transcript = data.get('raw_transcript')

        try:
            utterances = ""
            entities =""
            # Retrieve the meeting based on the provided meeting_id
            meeting = Meeting.objects.get(pk=meeting_id)
            final_transcript = process_transcription(entities,utterances,meeting.meeting_id)
            print('test',final_transcript)
            # Create a new Transcript object with the retrieved data
            transcript = Transcript(
                meeting_id=meeting.meeting_id,
                raw_transcript=final_transcript
            )

            # Save the transcript object
            transcript.save()

            # Return a JSON response indicating success
            return JsonResponse({'message': 'Transcript created successfully.'}, status=201)
        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)


@csrf_exempt
def create_transcript(request,meeting_id):
    if request.method == 'POST':
        final_transcript =process_transcription(meeting_id)
        final_transcript = json.loads(final_transcript)
        return JsonResponse(final_transcript, safe=False)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def transcription_view(request, meeting_id):
    if request.method == 'GET':
        try:
            transcript = Transcript.objects.get(meeting_id=meeting_id)
            raw_transcript = json.loads(transcript.raw_transcript)
            raw_transcript = [entry for entry in raw_transcript if "meeting_id" not in entry]
            print(raw_transcript)
            response_data = {
                "meeting_id": meeting_id,
                "transcript": raw_transcript
            }
            return JsonResponse(response_data, safe=False)
        except Transcript.DoesNotExist:
            return JsonResponse({'error': 'Meeting does not exist.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def priority_list(request):
    if request.method == 'GET':
        priorities = Priority.objects.all()
        data = [{'priority_id': priority.priority_id, 'name': priority.name,'value':priority.value} for priority in priorities]
    return JsonResponse(data, safe=False)

@csrf_exempt
def status_list(request):
    if request.method == 'GET':
        status_lists = Status.objects.all()
        data = [{'status_id': status.status_id, 'name': status.name,'value': status.value} for status in status_lists]
    return JsonResponse(data, safe=False)

@csrf_exempt
def users_list(request):
    if request.method == 'GET':
        user_lists = meeting_user_details.objects.all()
        data = [{'id': users.id, 'name': users.name,'profile_pic': users.profile_pic} for users in user_lists]
    return JsonResponse(data, safe=False)

@csrf_exempt
def meeting_comments(request, meeting_id):
    if request.method == 'GET':
        meeting_comments = Comments.objects.filter(meeting_id=meeting_id)
        data = [{'id': comment.id, 'name': comment.name, 'comments': comment.comments, 'profile_pics': comment.profile_pics} for comment in meeting_comments]
        response = {
            "total_count": len(data),
            "comments": data
        }
        return JsonResponse(response, safe=False)





