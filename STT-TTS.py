import speech_recognition as sr
import pyttsx3

def main():
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
        print('Command received')
        
        try:
            command = listener.recognize_google(voice)

            #if 'google' in command:
            print(command)
            engine.say(command)
            engine.runAndWait()

        except:
            print('error')
            pass

if __name__ == '__main__':
    main()