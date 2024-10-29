import os
import time
from pydub import AudioSegment

def resample_wav_to_16khz(input_file, output_file):
    audio = AudioSegment.from_wav(input_file)
    audio = audio.set_frame_rate(16000)
    audio.export(output_file, format="wav")


def create_audio_file_path(directory="recordings", prefix=""):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)    
    # Generate a timestamped filename
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"audio_{prefix}{timestamp}.wav"
    file_path = os.path.join(directory, filename)
    return file_path

def save_audio_to_wav(audio_data, directory="recordings"):
    file_path = create_audio_file_path(directory)

    # Save the audio data as a .wav file
    with open(file_path, "wb") as f:
        f.write(audio_data.get_wav_data())

    print(f"Audio saved as {file_path}")
    return file_path