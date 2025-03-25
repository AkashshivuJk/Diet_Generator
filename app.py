import os
from flask import Flask, request, jsonify, render_template
import requests


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_diet():
    try:
        # Get API key from environment variable
        API_KEY = 'YOUR_GEMINI_API'
        if not API_KEY:
            return jsonify({"success": False, "error": "API key not configured"})

        API_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}'

        # Get data from request
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['height', 'weight', 'age', 'gender', 'preferences', 'goal']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "error": f"Missing required field: {field}"})

        # Prepare request body for Gemini API
        request_body = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Create a detailed weekly diet plan. Details: Height {data['height']} cm, Weight {data['weight']} kg, Age {data['age']} years, Gender {data['gender']}, Goal {data['goal']}, Dietary Preference {data['preferences']}. Provide a comprehensive 7-day meal plan with breakfast, lunch, dinner, and snacks that meets the specified nutritional goals,also, you should  give the approximate amount of  nutrients(like carbs,protein,vitamins,fats) in each Meal."
                        }
                    ]
                }
            ]
        }

        # Make API request
        response = requests.post(API_URL, json=request_body)
        response.raise_for_status()  # Raise an exception for bad responses
        
        response_data = response.json()
        
        # Extract diet plan
        diet_suggestions = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', 'No diet suggestions available.')

        return jsonify({"success": True, "message": diet_suggestions})

    except requests.RequestException as e:
        return jsonify({"success": False, "error": f"API request failed: {str(e)}"})
    except Exception as e:
        return jsonify({"success": False, "error": f"An unexpected error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)