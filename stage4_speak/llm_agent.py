import base64
from openai import OpenAI
from utils.audio_utils import create_audio_file_path
client = OpenAI()


SYSTEM_PROMPT = """Jsi Tomáš, užitečný domácí sluha a asistent. 
Oslovuj uživatele uctivě a s respektem. Oslovuj ho pane. Tvůj uživatel se jmenuje Vráťa a je to počítačový mág.
Tvoje výstupy jsou v audio podobě, takže drž své odpovědi velmi krátké.
"""

msg_history = []

def think(text):
    global msg_history
    msg_history.append({"role": "user", "content": text})
    completion = client.chat.completions.create(
        model="gpt-4o",
        modalities=["text"],
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + msg_history
        )
    if completion.choices[0] is not None:
        if completion.choices[0].message is not None:
            msg_history.append({"role": "assistant", "content": completion.choices[0].message.content})    
    
    return completion.choices[0].message.content