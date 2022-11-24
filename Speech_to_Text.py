import speech_recognition as sr

def speech_to_text():
    listener = sr.Recognizer()
    command = ""
    
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        print('Say something')
        voice = listener.listen(source)
                
        try:
            command = listener.recognize_google(voice)
            print('Command received')
            print(command)
        
        except Exception as e:
            print(e)
            pass
    
    return command
    
