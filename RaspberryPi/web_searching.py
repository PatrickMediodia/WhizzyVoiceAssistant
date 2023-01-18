import subprocess
from text_to_speech import gtts_speak
from google_assistant import run

def start_google_assistant(command):
    device_model_id = "whizzy-raspberry-pi"
    device_id = "whizzy-1d843"
    
    run.main(command, device_model_id, device_id)