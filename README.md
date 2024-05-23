# Mistral Function Calling Test Project

This project demonstrates the use of the latest Mistral v0.3 model for handling function calling. The services are implemented using Flask, and the main application orchestrates calls to these microservices.

## Project Structure

- `cats.py`: Flask app for the cat facts microservice.
- `weather.py`: Flask app for the weather microservice.
- `main.py`: Main application that interacts with the microservices.
- `functions.json`: JSON file storing data about callable functions.

## Requirements

- Python 3.8+
- Flask
- Requests

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/100xlongx/ollama-function-calling-sample.git
   cd ollama-function-calling-sample
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Microservices

### Cat Facts Microservice

1. Navigate to the project directory.
2. Run the `cats.py` Flask app:
   ```sh
   python cats.py
   ```
3. The cat facts microservice will be available at `http://localhost:5002`.

### Weather Microservice

1. Open a new terminal window.
2. Navigate to the project directory.
3. Run the `weather.py` Flask app:
   ```sh
   python weather.py
   ```
4. The weather microservice will be available at `http://localhost:5001`.

## Running the Main Application

1. Ensure both microservices (`cats.py` and `weather.py`) are running.
2. Run the `main.py` script:
   ```sh
   python main.py
   ```

## Using the Application

The main application uses predefined functions stored in `functions.json` to interact with the microservices. Below is an example of how the JSON structure looks:

```json
[
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "format": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Infer this from the user's location."
                    }
                },
                "required": ["location", "format"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cat_facts",
            "description": "Get a random cat fact",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "The number of cat facts to return"
                    }
                },
                "required": ["amount"]
            }
        }
    }
]
```

### Example Usage

1. To get the current weather in San Francisco:
   ```sh
   python main.py
   ```

   This will call the weather microservice and print the current weather data.

2. To get a random cat fact:
   ```sh
   python main.py
   ```

   This will call the cat facts microservice and print a random cat fact.

## Notes

- Ensure the microservices are running before executing the main application.
- The `functions.json` file can be modified to add more functions as needed.
- The main application demonstrates how to handle API requests and process responses from microservices.

## License

This project is licensed under the MIT License