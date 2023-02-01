import speech_recognition as sr

r = sr.Recognizer()

file_audio = sr.AudioFile('out.wav')

with file_audio as source:
    audio_text = r.record(source)

print(type(audio_text))
print(r.recognize_google(audio_text))