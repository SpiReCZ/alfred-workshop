import base64
import json
from openai import OpenAI
from utils.audio_utils import create_audio_file_path
client = OpenAI()


SYSTEM_PROMPT = """Jsi Tomáš, užitečný domácí sluha a asistent. 
Oslovuj uživatele uctivě a s respektem. Oslovuj ho pane. Tvůj uživatel se jmenuje Vráťa a je to počítačový mág.
Tvoje výstupy jsou v audio podobě, takže drž své odpovědi velmi krátké.
"""


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Získá aktuální počasí pro zadané město.",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Město, pro které chceš získat počasí."
                    }
                },
                "required": ["city"],
                "additionalProperties": False
            }
        }
    }    
]

msg_history = []

def _call_llm(msg):
    global msg_history
    msg_history.append(msg)
    print ("history:")
    # pretty print the history
    print(json.dumps(msg_history, indent=4))
    completion = client.chat.completions.create(
        model="gpt-4o",
        modalities=["text"],
        tools=TOOLS,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
        ] + msg_history
        )

    print("completion:")
    print(completion)
    if completion.choices[0] is not None:
        if completion.choices[0].message is not None:
            if completion.choices[0].message.tool_calls is not None:
                completion.choices[0].message.tool_calls
                msg_history.append({"role": "assistant", "tool_calls": [completion.choices[0].message.tool_calls[0].to_dict()]})
            elif completion.choices[0].message.content is not None:
                msg_history.append({"role": "assistant", "content": completion.choices[0].message.content})
        
        
    return completion

def _format_tool_call_response_msg(call_id, content_dict):
    return {
        "role": "tool",
        "content": json.dumps(content_dict),
        "tool_call_id": call_id
    }


def _get_weather(params):
    city = params["city"]
    tool_response_content = {"temperature": "25 stupnňů", "city": city, "weather": "slunečno s tornády"}
    return tool_response_content


TOOL_FUNC_MAP = {
    "get_weather": _get_weather
}


def think(text):
    resolved = False
    completion = _call_llm({"role": "user", "content":text})
    while not resolved:
        if completion.choices[0].message.tool_calls is not None and completion.choices[0].message.tool_calls[0] is not None:
            resolved = False
            tool_call = completion.choices[0].message.tool_calls[0]
            tool_call_id = tool_call.id
            name = tool_call.function.name
            params = json.loads(tool_call.function.arguments)
            tool_func = TOOL_FUNC_MAP[name]
            tool_response_content = tool_func(params)
            tool_response_msg = _format_tool_call_response_msg(tool_call_id, tool_response_content)
            print("tool_response_msg:")
            print(tool_response_msg)
            completion = _call_llm(tool_response_msg)
        else:
            # audio_file_path = create_audio_file_path("audio_responses", "response_")
            # wav_bytes = base64.b64decode(completion.choices[0].message.audio.data)
            # with open(audio_file_path, "wb") as f:
            #     f.write(wav_bytes)
            resolved = True 
        return completion.choices[0].message.content