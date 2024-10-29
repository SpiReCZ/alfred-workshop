from openai import OpenAI
client = OpenAI()


SYSTEM_PROMPT = """ Jsi Tomáš, užitečný domácí sluha a asistent. 
Oslovuj uživatele uctivě a s respektem. Oslovuj ho pane. Tvůj uživatel se jmenuje Vráťa a je to počítačový mág.
"""

msg_history = []

def think(text):
    global msg_history
    msg_history.append({"role": "user", "content": text})
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + msg_history
        )
    return completion.choices[0].message.content