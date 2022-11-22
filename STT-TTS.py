from ctypes import *
from contextlib import contextmanager
import speech_recognition as sr
import pyttsx3

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

def main():
    with noalsaerr():
        engine = pyttsx3.init('espeak')

        #set voice type
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        #set talking rate
        engine.setProperty('rate', 75)
        
        listener = sr.Recognizer()

        engine.say('Hello I am Whizzy, your personal assistant')
        engine.runAndWait()

        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source)
            print('Say something')
            voice = listener.listen(source)
            
            try:
                command = listener.recognize_google(voice)
                print('Command received')
                
                #if 'google' in command:
                print(command)
                engine.say(command)
                engine.runAndWait()

            except Exception as e:
                print(e)
                pass

if __name__ == '__main__':
    main()