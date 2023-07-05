import requests
import json
import time
# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap
import openai
import json
from collections import defaultdict

# django imports
from django.http import HttpResponse
#from .recording_transcription.transcript import process_transcription

from user_authentication.models import User, Session
from recording_transcription.models import Meeting, Transcript
from django.shortcuts import get_object_or_404

def get_transcript_raw(meeting_id):
    transcript = get_object_or_404(Transcript, meeting_id=meeting_id)
    transcript_raw = transcript.raw_transcript
    return transcript_raw

# maximum tokens allowed for GPT-3
max_tokens = 4096  
# keep a buffer for response tokens. Let's assume 100 tokens for the completion
buffer_tokens = 100  
# calculate the maximum tokens we can use for the prompt
max_prompt_tokens = max_tokens - buffer_tokens

import re
from collections import defaultdict

def calculate_speaking_time(transcript):
    # Regex pattern to match the speaker and timestamps
    # this pattern will extract each speaker's name and their start and end times
    speakers = defaultdict(lambda: {"audio_breakpoints": {"start": [], "end": []}, "talk_time": 0})

    # extract data from the transcript and populate the `speakers` dict
    for details in transcript:
        #print('Item:', item)
        speaker = 'tushar'#item["speaker"]
        #print('Speaker:', speaker)
        print('Start Time:', details["start_time"])
        start, end, name = details["start_time"], details["end_time"], speaker
        speakers[name]["audio_breakpoints"]["start"].append(start)
        speakers[name]["audio_breakpoints"]["end"].append(end)
        speakers[name]["talk_time"] += end - start  # assuming times are in the same unit (e.g., seconds)

        if not isinstance(transcript, list):
            transcript = [transcript]

    # calculate total talk time to later compute percentages
    total_talk_time = sum(speaker["talk_time"] for speaker in speakers.values())

    # create the final output
    output = {
        "users_audio_breakpoints": [
            {
                "name": name,
                "avatar": "https://photos.com",
                "username": name.lower().replace(" ", ""),
                "audio_breakpoints": data["audio_breakpoints"],
                "talk_time": round(data["talk_time"] / total_talk_time * 100, 2),  # percentage of total talk time
            }
            for name, data in speakers.items()
        ]
    }

    return output

def key_labels(transcript):
    final_transcript = transcript
    #trancript_object = transcript.objects.get()
    prompt = final_transcript#trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nGenerate 10 labels or tags that describe the transcript suitable to the meeting comma seperated.",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )

    if response: 
        output = response.choices[0].text.strip()
        return output
    else:
        return "None"
    

def audio_breakpoints(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    transcript_data = json.loads(final_transcript)
    return calculate_speaking_time(transcript_data)

def meeting_key_labels(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    meeting_labels = key_labels(final_transcript)

    # split the labels by comma and remove any leading/trailing spaces
    return [label.strip() for label in meeting_labels.split(',')]
    
    
    
    
    
