import requests
import json
import time
# use the Python textwrap library to split the text into chunks of `max_prompt_tokens` length
import textwrap
import openai

# django imports
from django.http import HttpResponse
#from .recording_transcription.transcript import process_transcription

# maximum tokens allowed for GPT-3
max_tokens = 4096  
# keep a buffer for response tokens. Let's assume 100 tokens for the completion
buffer_tokens = 100  
# calculate the maximum tokens we can use for the prompt
max_prompt_tokens = max_tokens - buffer_tokens
#process_transcription = ""
def get_action_items(request):
    final_transcript = "wejfn"
    #trancript_object = transcript.objects.get()
    prompt = final_transcript#trancript_object.transcript_raw
    prompt_chunks = textwrap.wrap(prompt, max_prompt_tokens)

    openai.api_key = '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'
    response = None
    for chunk in prompt_chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk + "\nGive me a action items of the meeting in less than 120 words",
            temperature=0.2,
            #max_tokens=150,
            max_tokens=buffer_tokens
        )
    if response: 
        output = response.choices[0].text.strip()
        return output
    else:
        return "None"