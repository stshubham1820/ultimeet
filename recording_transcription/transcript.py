import requests
import json
import time
#from pydub import AudioSegment

base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "3791eb83c72547c88214e5f95449a4c2"
}

with open("/Users/sudarshanchavan/Desktop/Projects/meetings-master-4/ultimeet_backend/ultimeet/recording_transcription/Panel_Discussion_AI.mp3", "rb") as f:
  response = requests.post(base_url + "/upload",
                          headers=headers,
                          data=f)

upload_url = response.json()["upload_url"]

#audio = AudioSegment.from_file("audio.wav")

data = {
    "audio_url": upload_url,
    "speaker_labels": True,
    "entity_detection": True,
    "speakers_expected": 2
}

url = base_url + "/transcript"
response = requests.post(url, json=data, headers=headers)

transcript_id = response.json()['id']
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

utterances = ""
entities = ""

while True:
  transcription_result = requests.get(polling_endpoint, headers=headers).json()

  if transcription_result['status'] == 'completed':
    #transcription_result = transcription_result['transcription_result']
    entities = transcription_result['entities']
    utterances = transcription_result['utterances']
    #print(f"Entities {entities}")
    #print(utterances)
    # Iterate through each utterance and print the speaker and the text they spoke

    def process_utterance(utterance):
        resultTranscript = []
        #resultTranscript = ""
        for utterance in utterances:
            for entity in entities:
                if(entity['entity_type'] == 'person_name'):
                #print("Entity Type:", entity['entity_type'])
                    #print("Text:", entity['text'])
                #print()  # Add an empty line between entities
                    pass
            #break
            speaker = utterance['speaker']
            text = utterance['text']
            start_time = utterance['start']
            end_time = utterance['end']
            
            #segment_audio = audio[start_time:end_time]
            #segment_audio.export(f"{speaker}.wav", format="wav")
        
            resultTranscript.append({
            'avatar': 'https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50.jpg',
            'speaker': speaker,
            'text': text,
            'start_time': start_time,
            'end_time': end_time
        })
        #resultTranscript.append({'meeting_id': 1})
            #print(f"Speaker {speaker}:: {text}")
            #resultTranscript += f"Speaker {speaker}:: {text}\n"  # append new string with a newline character
        return json.dumps(resultTranscript,ensure_ascii=False)   
    break

  elif transcription_result['status'] == 'error':
    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

  else:
    time.sleep(3)

def process_transcription():
    finaltrans = process_utterance(utterances)
    #print(f"final Transcript:",finaltrans)
    updated_transcript, updated_utterances = find_speakers(utterances,entities,finaltrans)

    return updated_transcript

def find_speakers(utterances, entities, transcript):
    for i in range(len(utterances)):  # assuming utterances and entities have the same length
        entity = entities[i]
        if entity['entity_type'] == 'person_name':
            new_speaker = entity['text']
            utterance = utterances[i]
            speaker = utterance['speaker']
            transcript = update_speaker_in_transcript(transcript, speaker, new_speaker)
            utterance['speaker'] = new_speaker  # Update the speaker label in the utterance
    return transcript, utterances

def update_speaker_in_transcript(transcript, old_speaker, new_speaker):
    if len(old_speaker) == 1:  # Check if speaker's name is a single character
        updated_transcript = transcript.replace(old_speaker, new_speaker)
        return updated_transcript
    else:
        return transcript  # Return original transcript if speaker's name is not a single character






#print(updated_transcript)
#print("Updated Transcript:", updated_transcript)
#print("Updated Utterances:", updated_utterances)

