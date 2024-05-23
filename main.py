import requests
import json
import re

with open("functions.json", "r") as file:
    tool_set = json.load(file)

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

def process_tool_call(data):
    for call in data:
        if call["name"] == "get_cat_facts":
            # Extract the amount parameter from the tool call
            amount = call["arguments"]["amount"]
            
            # Make a request to your cat facts API
            cat_facts_url = f"http://localhost:5002/api/cat_facts?amount={amount}"
            cat_facts_response = requests.get(cat_facts_url)
            
            # Parse the response from the cat facts API
            cat_facts = cat_facts_response.json()
            
            # Print the cat facts
            print("Cat Facts:")
            for fact in cat_facts:
                print(fact)
        if call["name"] == "get_current_weather":
            # Extract the location and format parameters from the tool call
            location = call["arguments"]["location"]
            format = call["arguments"]["format"]
            
            # Make a request to your weather API
            weather_url = f"http://localhost:5001/api/weather"
            weather_data = {
                "location": location,
                "format": format
            }
            weather_response = requests.post(weather_url, json=weather_data)
            
            # Parse the response from the weather API
            weather = weather_response.json()
            
            # Print the weather data
            print("Weather Data:")
            print(f"Location: {weather['location']}")
            print(f"Temperature: {weather['temperature']} {weather['unit']}")
            print(f"Description: {weather['description']}")

ollama_url = "http://localhost:11434/api/generate"

prompt = "What is the weather like today in San Francisco"
response = make_request(prompt, tool_set, ollama_url)
tool_calls = extract_tool_calls(response['response'])

if tool_calls:
    print("Tool Calls", tool_calls)
    process_tool_call(tool_calls)

prompt = "Tell me a single cat fact."
response = make_request(prompt, tool_set, ollama_url)
tool_calls = extract_tool_calls(response['response'])

if tool_calls:
    print("Tool Calls", tool_calls)
    process_tool_call(tool_calls)

prompt = "Tell me multiple cat facts."
response = make_request(prompt, tool_set, ollama_url)
tool_calls = extract_tool_calls(response['response'])

if tool_calls:
    print("Tool Calls", tool_calls)
    process_tool_call(tool_calls)