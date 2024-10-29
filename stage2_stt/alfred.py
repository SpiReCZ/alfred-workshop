from dotenv import load_dotenv
load_dotenv()
import time
from hotword_detection import recognize_hotword, setup_audio_recognition
from sst import speech_to_text


def main():
    microphone, recognizer = setup_audio_recognition()
    while True:
        time.sleep(0.01)
        hotword_text, audio_file = recognize_hotword(microphone, recognizer)
        input_text = speech_to_text(audio_file)

main()