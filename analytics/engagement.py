import requests
import json
import time
# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap
import openai
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

def calculate_talk_time_percentages(transcript):
    total_talk_time = 0
    speaker_talk_time = {}

    for entry in transcript:
        try:
            talk_time = entry['end_time'] - entry['start_time']
            total_talk_time += talk_time

            if entry['speaker'] in speaker_talk_time:
                speaker_talk_time[entry['speaker']] += talk_time
            else:
                speaker_talk_time[entry['speaker']] = talk_time
        except KeyError as e:
            print(f"KeyError: {e} for entry: {entry}")

    # Calculate and print speaker talk time percentages
    speaker_percentages = {}
    for speaker, talk_time in speaker_talk_time.items():
        percentage = (talk_time / total_talk_time) * 100
        speaker_percentages[speaker] = percentage

    # Calculate average speaker percentage
    avg_speaker_percentage = sum(speaker_percentages.values()) / len(speaker_percentages)

    return speaker_percentages, avg_speaker_percentage


def engagement_levels(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    transcript_data = json.loads(final_transcript)
    speaker_percentages, avg_speaker_percentage = calculate_talk_time_percentages(transcript_data)
    return speaker_percentages, avg_speaker_percentage


    
    
    
    
