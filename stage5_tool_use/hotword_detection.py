import json
import os
import shlex
import subprocess
import sys
import time
import speech_recognition as sr
from vosk import Model
from pydub import AudioSegment
from utils.audio_utils import resample_wav_to_16khz, save_audio_to_wav
from utils.text_utils import find_trigger_word


MODEL_PATH = 'models/vosk-model-small-cs-0.4-rhasspy'

HOTWORDS = {
    "alfred": ["Tomáši", "tomáš"]
}


class VoskRecognizer(sr.Recognizer):
    def __init__(self, model_path):
        super().__init__()
        self.vosk_model = Model(model_path)

def _calibrate_microphone(recognizer: sr.Recognizer, microphone: sr.Microphone):
    print("Mic: Calibrating...")
    recognizer.adjust_for_ambient_noise(microphone, duration=2)
    recognizer.dynamic_energy_threshold = False
    print("Mic: Calibrated!")


def _execute_whisper(audio_file_name):
    resample_wav_to_16khz(audio_file_name, audio_file_name)
    command = f"./whisper.cpp/main -m ./whisper.cpp/models/ggml-base.bin --no-timestamps -f ./{audio_file_name}"
    # Split the command string into a list of command arguments using shlex.split
    cmd = shlex.split(command)
    # Run the command and capture the output
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("WHISPER RESULT:  \n")
    print.debug(result)
    # Return the output (stdout), and also return the error (stderr) if any
    return result.stdout, result.stderr


def setup_audio_recognition():
    recognizer = VoskRecognizer(MODEL_PATH)
    recognizer.operation_timeout = 200
    recognizer.pause_threshold = 0.5
    recognizer.energy_threshold = 4000
    microphone = sr.Microphone()
    with microphone as source:
        _calibrate_microphone(recognizer, microphone)
    return (microphone,recognizer)

def recognize_hotword(microphone: sr.Microphone, recognizer: sr.Recognizer):
    with microphone as source:
        while True:
            print("Listening for hotword...")
            audio = recognizer.listen(source, phrase_time_limit=10,)
            audio_file_path = save_audio_to_wav(audio)
            print("Listened.")
            # Vosk recognizer
            text_json = recognizer.recognize_vosk(audio, language='cs-CZ')
            text = json.loads(text_json)["text"]
            print("Got text from vosk")
            print(f"You said: {text}")
            # Whisper recognizer
            #text = _execute_whisper(audio_file_path)
            trigger_word = find_trigger_word(text, HOTWORDS)
            if trigger_word is not None and trigger_word[0] == "alfred":
                print("Hotword detected!")
                return (text, audio_file_path)
