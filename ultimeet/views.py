# views.py

from django.shortcuts import render


recording = None
filename = 'recording.wav'

def home(request):
    return render(request, 'home.html')

def start_recording(request):
    global recording
    recording = sd.rec(int(5 * 44100), channels=2)
    sd.wait()
    return render(request, 'home.html', {'message': 'Recording started.'})

def stop_recording(request):
    global recording
    if recording is not None:
        sf.write(filename, recording, 44100, 'PCM_24')
        recording = None
        return render(request, 'home.html', {'message': 'Recording stopped and saved as recording.wav.'})
    else:
        return render(request, 'home.html', {'message': 'No recording to stop.'})

def process_speech(request):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        if text.lower() == "start meeting":
            return start_recording(request)
        elif text.lower() == "stop meeting":
            return stop_recording(request)
        else:
            return render(request, 'home.html', {'message': 'Unknown command.'})
    except sr.UnknownValueError:
        return render(request, 'home.html', {'message': 'Unable to recognize speech.'})
