import requests
import json
import re
import inspect

with open("functions.json", "r") as file:
    tool_set = json.load(file)

def make_request(prompt, tool_set, url):
    request_payload = {
        "model": "mistral:v0.3",
        "prompt": f"[AVAILABLE_TOOLS] {json.dumps(tool_set)} [/AVAILABLE_TOOLS][INST] {prompt} [/INST]",
        "raw": True,
        "stream": False,
        "tool_choice": "required"
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

def get_president(year):
    if year == "2004":
        return "George W. Bush"
    elif year == "2008":
        return "Barack Obama"
    elif year == "2012":
        return "Barack Obama"
    elif year == "2016":
        return "Donald Trump"
    else:
        return "Unknown"
    
def get_cat_facts(amount):
    cat_facts_url = f"http://localhost:5002/api/cat_facts?amount={amount}"
    cat_facts_response = requests.get(cat_facts_url)
    cat_facts = cat_facts_response.json()
    return cat_facts

def get_current_weather(location, format):
    # Call the weather API
    weather_url = f"http://localhost:5001/api/weather"
    weather_data = {
        "location": location,
        "format": format
    }
    weather_response = requests.post(weather_url, json=weather_data)
    weather = weather_response.json()
    return weather

ollama_url = "http://localhost:11434/api/generate"

available_functions = {
    "get_current_weather": get_current_weather,
    "get_cat_facts": get_cat_facts,
    "get_president": get_president
}

prompt = "Whos the president in 2004?"
response = make_request(prompt, tool_set, ollama_url)
tool_calls = extract_tool_calls(response['response'])

if tool_calls:
    try:
        for call in tool_calls:
            function_name = call["name"]
            function = available_functions.get(function_name)
            if function:
                sig = inspect.signature(function)
                arguments = call["arguments"]
                try:
                    bound_args = sig.bind(**arguments)
                    result = function(*bound_args.args, **bound_args.kwargs)
                    print(result)
                except TypeError as e:
                    print(f"Argument mismatch for function '{function_name}': {e}")
            else:
                print(f"Function '{function_name}' not found")
                print(call)
    except Exception as e:
        print(e)