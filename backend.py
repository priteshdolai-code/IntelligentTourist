# Import the necessary modules
from flask import Flask, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient
from flask_cors import CORS

# Create a Flask app instance
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Define the endpoint for handling requests from the frontend
@app.route('/predict_intent', methods=['POST'])
def predict_intent():
    # Parse the JSON data from the request sent by the frontend
    request_data = request.json

    # Extract the intent predicted by the CLU model from the request data
    predicted_intent = request_data.get('intent')

    # Initialize the CLU client with your Azure CLU API credentials
    clu_endpoint = "https://intelllang.cognitiveservices.azure.com/"
    clu_key = "283134932e964201bce04e1af99ae71c"
    project_name = "IntellTour"
    deployment_name = "IntellTour"
    clu_client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))

    # Analyze the predicted intent using the CLU model
    with clu_client:
        result = clu_client.analyze_conversation(
            task={
                "kind": "Conversation",
                "analysisInput": {
                    "conversationItem": {
                        "participantId": "1",
                        "id": "1",
                        "modality": "text",
                        "language": "en",
                        "text": predicted_intent
                    },
                    "isLoggingEnabled": False
                },
                "parameters": {
                    "projectName": project_name,
                    "deploymentName": deployment_name,
                    "verbose": True
                }
            }
        )

    # Extract the top intent from the result
    top_intent = result["result"]["prediction"]["topIntent"]

    # Map the top intent to the corresponding state on the SVG map
    state_mapping = {
        'Andhra Pradesh': 'INAP',
        'Arunachal Pradesh': 'INAR',
        'Assam': 'INAS',
        'Bihar' : 'INBR',
        'Chattisgarh': 'INCT',
        'Goa': 'INGA',
        'Gujarat': 'INGJ',
        'Haryana': 'INHR',
        'Himachal Pradesh': 'INHP',
        'Jharkhand': 'INJH',
        'Karnataka': 'INKA',
        'Kerala': 'INKL',
        'Ladakh': 'INLA',
        'Lakshadweep': 'INLD',
        'Madhya Pradesh': 'INMP',
        'Maharashtra': 'INMH',
        'Manipur': 'INMN',
        'Meghalaya': 'INML',
        'Mizoram': 'INMZ',
        'Nagaland': 'INNL',
        'Odisha': 'INOR',
        'Punjab': 'INPB',
        'Rajasthan': 'INRJ',
        'Sikkim': 'INSK',
        'Tamil Nadu': 'INTN'
        # Add mappings for other intents and states
    }

    # Get the corresponding state for the predicted intent
    predicted_state = state_mapping.get(top_intent)

    # Prepare the response data to be sent back to the frontend
    response_data = {
        "state": predicted_state
        # You can add more data to the response if needed
    }

    # Convert the response data to JSON format and send it back to the frontend
    return jsonify(response_data)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
