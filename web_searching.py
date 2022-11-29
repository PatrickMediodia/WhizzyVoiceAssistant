import subprocess
from text_to_speech import gtts_speak

def start_google_assistant(command):
    google_assistant_response = subprocess.getoutput(f'python3 google_assistant/run.py --command "{command}" --device-model-id "whizzy-raspberry-pi" --device-id "whizzy-1d843"')
    if google_assistant_response != '':
        print(google_assistant_response)
        gtts_speak(google_assistant_response)
    else:
        gtts_speak('Sorry, I cannot process that command')
