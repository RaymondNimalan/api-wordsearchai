from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging
from openai import OpenAI

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/test', methods=['POST'])
def test_route():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    return jsonify({'response': f"Received your message: {data['message']}"})


@app.route('/api/generate', methods=['POST'])
def generate_game():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-3.5-turbo",
        )

        generated_text = response.choices[0].message.content
        logging.debug(f"Generated text: {generated_text}")

        return jsonify({'generated_text': generated_text})

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)



