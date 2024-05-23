from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/weather', methods=['POST'])
def get_current_weather():
    data = request.json
    location = data.get('location')
    format = data.get('format')
    
    # Mock response
    weather_data = {
        "location": location,
        "temperature": "20",
        "unit": format,
        "description": "Partly cloudy"
    }
    
    return jsonify(weather_data)

if __name__ == '__main__':
    app.run(port=5001)
