import requests
import json
import re

def make_request(prompt, tool_set, url):
    request_payload = {
        "model": "mistral:v0.3",
        "prompt": f"[AVAILABLE_TOOLS] {json.dumps(tool_set)} [/AVAILABLE_TOOLS][INST] {prompt} [/INST]",
        "raw": True,
        "stream": False
    }
    response = requests.post(url, data=json.dumps(request_payload), headers={"Content-Type": "application/json"})
    return response.json()

def extract_tool_calls(response_text):
    match = re.search(r'\[TOOL_CALLS\]\s*(\[.*?\])', response_text, re.DOTALL)
    if match:
        tool_calls_json = match.group(1)
        tool_calls = json.loads(tool_calls_json)
        return tool_calls
    return None

with open("functions.json", "r") as file:
    tool_set = json.load(file)

url = "http://localhost:11434/api/generate"

prompt1 = "What is the weather like today in San Francisco"
response1 = make_request(prompt1, tool_set, url)
tool_calls1 = extract_tool_calls(response1['response'])
print("Tool Calls 1:", tool_calls1)

# Example request 2
prompt2 = "Tell me a cat fact"
response2 = make_request(prompt2, tool_set, url)
tool_calls2 = extract_tool_calls(response2['response'])
print("Tool Calls 2:", tool_calls2)