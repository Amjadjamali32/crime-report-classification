from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# HuggingFace API details
API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
API_TOKEN = "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"

# Headers for HuggingFace API
headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}

# Function to query the Hugging Face model
def query_model(crime_report):
    response = requests.post(
        API_URL,
        headers=headers,
        json={
            "inputs": crime_report,
            "parameters": {
                "candidate_labels": ["theft", "robbery", "fraud", "vandalism", "assault", "miscellaneous"]
            }
        }
    )
    return response.json()

# Endpoint for receiving crime report and returning classification
@app.route('/classify', methods=['POST'])
def classify_crime_report():
    data = request.get_json()

    if 'crimeReport' not in data:
        return jsonify({
            "success": False,
            "message": "Crime report not provided"
        }), 400

    crime_report = data['crimeReport']

    try:
        # Query the model for classification
        output = query_model(crime_report)
        labels = output['labels']
        scores = output['scores']

        # Get the predicted crime type with the highest score
        prediction_score = max(scores)
        predicted_crime_type = labels[scores.index(prediction_score)]

        # Threshold logic to classify as Miscellaneous if score is too low
        threshold = 0.5
        if prediction_score < threshold:
            predicted_crime_type = "Miscellaneous"

        return jsonify({
            "success": True,
            "description": crime_report,
            "crime_category": predicted_crime_type,
            "prediction_score": prediction_score
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)