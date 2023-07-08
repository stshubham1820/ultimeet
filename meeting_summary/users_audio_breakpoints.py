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
    speakers = defaultdict(lambda: {"audio_breakpoints": {"start": [], "end": []}, "talk_time": 0})

    for item in transcript:
        try:
            name, start, end = item.get("speaker"), item.get("start_time"), item.get("end_time")
        except AttributeError as e:
            print(f"Error processing transcript item: {item}. Error: {e}")
            continue
        if name is None or start is None or end is None:
            print(f"Missing data in transcript item: {item}")
            continue
            
        speakers[name]["audio_breakpoints"]["start"].append(start)
        speakers[name]["audio_breakpoints"]["end"].append(end)
        speakers[name]["talk_time"] += end - start  

    total_talk_time = sum(speaker["talk_time"] for speaker in speakers.values())

    output = {
        "users_audio_breakpoints": [
            {
                "name": name,
                "avatar": "https://photos.com",
                "username": name.lower().replace(" ", ""),
                "audio_breakpoints": data["audio_breakpoints"],
                "talk_time": round(data["talk_time"] / total_talk_time * 100, 2), 
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

    #openai.api_key = 'sk-m9XN22oM1nLBIR1ircsYT3BlbkFJZI9sjQ6DX3Lp'
    response = None
    
    output = "Productivity, Quality, Security, Availability, Diminishing Returns, FY 22 Direction, Mr Rates, Indicators, Agenda, Four Year Old"#response.choices[0].text.strip()
    return output   
        
    
    

def audio_breakpoints(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    transcript_data = json.loads(final_transcript)
    return calculate_speaking_time(transcript_data)

def meeting_key_labels(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    meeting_labels = key_labels(final_transcript)

    # split the labels by comma and remove any leading/trailing spaces
    return [label.strip() for label in meeting_labels.split(',')]
    
    
    
    
    
