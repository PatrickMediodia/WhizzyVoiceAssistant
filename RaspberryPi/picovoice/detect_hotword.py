import struct
import pyaudio
import pvporcupine

def detect_hotword():
    porcupine = None
    py_audio = None
    audio_stream = None

    try:
        porcupine = pvporcupine.create(
            access_key = '0wabvV6OPA1C6pGvDlM2e8e7NmR11B4uOh58tILLO7a5euM9LsE9Kg==',
            keyword_paths = ['picovoice/HeyWhizzyPi.ppn']
        )

        py_audio = pyaudio.PyAudio()
    
        audio_stream = py_audio.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
        
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
                            
            if keyword_index == 0:
                print('\nHey Whizzy detected')
                return True
            
    finally:
        if porcupine is not None:
            porcupine.delete()

        if audio_stream is not None:
            audio_stream.close()

        if py_audio is not None:
            py_audio.terminate()
                    
    return False