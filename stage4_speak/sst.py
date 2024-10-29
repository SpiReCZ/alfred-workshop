from openai import OpenAI
client = OpenAI()



def speech_to_text(audio_file_path):
    audio_file= open(audio_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        language="cs",
        file=audio_file
    )
    return transcription.text