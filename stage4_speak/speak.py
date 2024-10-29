from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI
from utils.audio_utils import create_audio_file_path
client = OpenAI()




def speak(text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        response_format="wav",
        input=text
    )
    audio_file_path = create_audio_file_path("audio_responses", "response_")
            # wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
            # with open(audio_file_path, "wb") as f:
            #     f.write(wav_bytes)
    response.stream_to_file(audio_file_path)
    audio = AudioSegment.from_wav(audio_file_path)
    play(audio)