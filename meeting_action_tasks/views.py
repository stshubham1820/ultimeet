from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .action_items import get_action_items
from recording_transcription.models import Meeting, Transcript
from meeting_action_tasks.models import ActionItem
from django.shortcuts import get_object_or_404
import textwrap
import openai
import json
import time
from django.core.exceptions import ObjectDoesNotExist


# maximum tokens allowed for GPT-3
max_tokens = 4096  
# keep a buffer for response tokens. Let's assume 100 tokens for the completion
buffer_tokens = 100  
# calculate the maximum tokens we can use for the prompt
max_prompt_tokens = max_tokens - buffer_tokens
#process_transcription = ""

def get_transcript_raw(meeting_id):
    transcript = get_object_or_404(Transcript, meeting_id=meeting_id)
    transcript_raw = transcript.raw_transcript
    return transcript_raw

# @csrf_exempt
# def action_items(request):
#     if request.method == 'POST':
#             get_actions = get_action_items(request)
#             return JsonResponse({'Action Items': get_actions})
            
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)



# Set up OpenAI API credentials
openai.api_key = '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'

@csrf_exempt
def generate_action_items(request,meeting_id):
    prompt_chunks = ""
    if request.method == 'POST':
        final_transcript = get_transcript_raw(meeting_id)
        prompt = final_transcript
        prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)
        #transcript = request.POST.get('transcript')

        # Generate action items using ChatGPT
        response = None
    generated_action_items = []
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"Generate action items with action item, name, owner, due date, status, priority, reporter:\n\nAction Items:\n\n{chunk}",
            max_tokens=100,
            n=5,  # Number of action items to generate
            temperature=0.7,
            stop=None,
            frequency_penalty=0.2
            #temperature=0.6
        )
        generated_action_items.append(response.choices[0].text.strip())

    # Concatenate the generated action items from all chunks
    action_items = '\n\n'.join(generated_action_items)

    # Process the action items and create a list of dictionaries
    result = []
    lines = action_items.split('\n\n')
    for line in lines:
        action_item = line.split('\n')
        item_dict = {}
        for item in action_item:
            if ':' in item:
                key, value = item.split(':', 1)
                item_dict[key.strip()] = value.strip()
        if item_dict:
            result.append(item_dict)

    meeting = Meeting.objects.get(pk=meeting_id)
    for item in result:
        name = result[1].get('Name')
        #name = item.get('Name')
        print("name",name)
        owner = item.get('Owner')
        due_on = item.get('Due Date')
        status = item.get('Status')
        priority = item.get('Priority')
        reporter = item.get('Reporter')
        
        # Get the second item from the result array
        #action_item_name = result[1].get('Name')
        if name is not None:
            action_item = ActionItem(
                meeting=meeting,
                name=name,
                owner=owner,
                due_on=due_on,
                status=status,
                priority=priority,
                reporter=reporter,
            )
            action_item.save()
    #print(name)
    
    # Convert the result to JSON format
    json_output = json.dumps(result, indent=4)
    print(json_output)
    
        # Process the response and extract action items
        

    return JsonResponse({'message': 'Action generated successfully.'}, status=200)

@csrf_exempt
@csrf_exempt
def get_action_item_by_id(request, action_item_id):
    if request.method == 'GET':
        try:
            action_item = ActionItem.objects.get(action_item_id=action_item_id)
            data = {
                'action_item_id': action_item.action_item_id,
                'name': action_item.name,
                'owner': action_item.owner,
                'reporter': action_item.reporter,
                'priority': action_item.priority,
                'due_on': action_item.due_on,
                'status': action_item.status,
                'actions': action_item.actions,
            }
            return JsonResponse(data, safe=False)
        except ActionItem.DoesNotExist:
            return JsonResponse({'error': 'Action item not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def update_action_item(request, action_item_id):
    if request.method == 'PUT' or request.method == 'PATCH':
        try:
            action_item = ActionItem.objects.get(pk=action_item_id)
            
            # Get the new values from the request data
            body = request.body.decode('utf-8')
            data = json.loads(body)
            name = data.get('name')
            owner = data.get('owner')
            reporter = data.get('reporter')
            priority = data.get('priority')
            due_on = data.get('due_on')
            status = data.get('status')
            actions = data.get('actions')
            dependencies = data.get('dependencies')
            comments = data.get('comments')
            reporter_profile_pic = data.get('reporter_profile_pic')
            owner_profile_pic = data.get('owner_profile_pic')

            # Update the action item
            action_item.name = name
            action_item.owner = owner
            action_item.reporter = reporter
            action_item.priority = priority
            action_item.due_on = due_on
            action_item.status = status
            action_item.actions = actions
            action_item.dependencies = dependencies
            action_item.comments = comments
            action_item.reporter_profile_pic = reporter_profile_pic
            action_item.owner_profile_pic = owner_profile_pic
            action_item.save()
            
            # Prepare the updated action item data for response
            response_data = {
                'action_item_id': action_item.action_item_id,
                'name': action_item.name,
                'owner': action_item.owner,
                'reporter': action_item.reporter,
                'priority': action_item.priority,
                'due_on': action_item.due_on,
                'status': action_item.status,
                'actions': action_item.actions,
                
            }
            return JsonResponse({'message': 'Action Item Updated successfully.'}, status=200)
        except ActionItem.DoesNotExist:
            return JsonResponse({'error': 'Action item not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

@csrf_exempt
def get_action_items_by_meeting_id(request, meeting_id):
    action_items = ActionItem.objects.filter(meeting_id=meeting_id)
    data = []
    for item in action_items:
        data.append({
            'action_item_id': item.action_item_id,
            'name': item.name,
            'owner': item.owner,
            'reporter': item.reporter,
            'priority': item.priority,
            'due_on': item.due_on,
            'status': item.status,
            'actions': item.actions,
            'reporter_profile_pic': item.reporter_profile_pic,
            'owner_profile_pic': item.owner_profile_pic,
        })
    return JsonResponse(data, safe=False)
        
        



