import requests
import json
import time


base_url = "https://api.assemblyai.com/v2"

headers = {
    "authorization": "3791eb83c72547c88214e5f95449a4c2"
}

def upload_audio(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(base_url + "/upload",
                                 headers=headers,
                                 data=f)
    print('Upload_URL::',response)
    upload_url = response.json()["upload_url"]
    
    return upload_url

def get_transcript(upload_url):
    print('Upload_URL::',upload_url)
    data = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "entity_detection": True,
        "speakers_expected": 2
    }

    url = base_url + "/transcript"
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        if "id" in response_json:
            transcript_id = response_json["id"]
            polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

            while True:
                transcription_result = requests.get(polling_endpoint, headers=headers).json()

                if transcription_result['status'] == 'completed':
                    entities = transcription_result['entities']
                    utterances = transcription_result['utterances']
                    return entities, utterances

                elif transcription_result['status'] == 'error':
                    raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

                else:
                    time.sleep(3)

        else:
            raise RuntimeError("Transcript ID not found in the response")

    else:
        error_message = response.json().get("error") or "Unknown error"
        raise RuntimeError(f"Transcription request failed with status code {response.status_code}: {error_message}")



def process_utterance(entities, utterances):
    resultTranscript = []
    for utterance in utterances:
        for entity in entities:
            if entity['entity_type'] == 'person_name':
                pass
        speaker = utterance['speaker']
        text = utterance['text']
        start_time = utterance['start']
        end_time = utterance['end']

        resultTranscript.append({
            'avatar': 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
            'speaker': speaker,
            'text': text,
            'start_time': start_time,
            'end_time': end_time
        })
        #resultTranscript.append({'meeting_id': 1})

    return json.dumps(resultTranscript, ensure_ascii=False)

def process_transcription(entities, utterances,meeting_id):
    print('uploadfile name:',meeting_id)
    file_path = "/Users/sudarshanchavan/Desktop/my_code/{}.wav".format(meeting_id)
    upload_url = upload_audio(file_path)
    entities, utterances = get_transcript(upload_url)
    finaltrans = process_utterance(entities, utterances)
    #print(f"final Transcript:",finaltrans)
    updated_transcript, updated_utterances = find_speakers(utterances,entities,finaltrans)
    

    print("Updated Transcript:", updated_transcript)
   
    
    return updated_transcript

def find_speakers(utterances, entities, transcript):
    for i in range(len(utterances)):
        if i < len(entities):  # Check if the index is within the range of entities
            entity = entities[i]
            if entity['entity_type'] == 'person_name':
                new_speaker = entity['text']
                print('new_speaker:',new_speaker)
                utterance = utterances[i]
                speaker = utterance['speaker']
                transcript = update_speaker_in_transcript(transcript, speaker, new_speaker)
                utterance['speaker'] = new_speaker
    return transcript, utterances


def update_speaker_in_transcript(transcript, old_speaker, new_speaker):
    if len(old_speaker) == 1:
        updated_transcript = transcript.replace(old_speaker, new_speaker)
        return updated_transcript
    else:
        return transcript


