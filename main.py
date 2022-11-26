from ALSA_handler import noalsaerr
from text_to_speech import gtts_speak
from speech_to_text import speech_to_text
from detect_hotword import detect_hotword
from smart_controls import start_smart_controls
from google_assistant.run import start_google_assistant
from interactive_discussion import start_interactive_discussion

modes = (
    'web searching',
    'smart control',
    'interactive discussion'
)
    
mode_map = {
    'web searching': start_google_assistant,
    'smart control': start_smart_controls,
    'interactive discussion': start_interactive_discussion
}

current_mode = modes[1]

def main():
    gtts_speak('Hello I am Whizzy, your personal assistant')
    
    with noalsaerr():
        while True:
            if detect_hotword():
                mode_map[current_mode]()
                
if __name__ == '__main__':
    main()