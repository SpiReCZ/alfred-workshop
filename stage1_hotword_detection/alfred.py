import time
from hotword_detection import recognize_hotword, setup_audio_recognition


def main():
    microphone, recognizer = setup_audio_recognition()
    while True:
        time.sleep(0.01)
        recognize_hotword(microphone, recognizer)
        

main()

