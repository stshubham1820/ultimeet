import requests
import json
import time

# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap
import openai

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
#process_transcription = ""
def meeting_agenda(meeting_id):
    final_transcript = get_transcript_raw(meeting_id)
    #trancript_object = transcript.objects.get()
    prompt = final_transcript#trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nAgenda of meeting in less than 12 words",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        output = response.choices[0].text.strip()
        return output
    else:
        return "None"