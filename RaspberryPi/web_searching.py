import os
import subprocess
from text_to_speech import gtts_speak
from google_assistant import run

def start_google_assistant(command):
    device_model_id = os.environ.get('DEVICE_MODEL_ID')
    device_id = os.environ.get('DEVICE_ID')
    
    run.main(command, device_model_id, device_id)