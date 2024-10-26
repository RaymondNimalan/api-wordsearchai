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
    settings = data.get('settings')

    if not settings:
        return jsonify({'error': 'Settings are required'}), 400
    
    topic = settings.get('topic')
    word_length = settings.get('wordLength')
    number_of_words = settings.get('numberOfWords')

    if not topic or not word_length or not number_of_words:
        return jsonify({'error': 'Unable to extract game settings'})


    try:
        prompt = f"""Prompt:

Create a JavaScript object for a word search game. The object should contain the following properties:

matrix: A 10x10 matrix filled with random uppercase letters. The matrix must include a selection of hidden words that can be placed:

Vertically (top to bottom or bottom to top)
Horizontally (left to right or right to left)
Diagonally (in any diagonal direction, both forwards and backwards)
Words may intersect with each other.
words: An array containing exactly 10 words, selected based on the specified settings. The words must:

Follow the chosen topic and length constraints.
Be positioned within the matrix according to the rules specified above.
settings: An object with the following editable properties:

topic: A string that specifies the category of words (e.g., "animals," "fruits," etc.).
wordLength: A string that indicates the desired word length category:
"short" (3-6 letters)
"medium" (3-9 letters)
"long" (3-12 letters)
numberOfWords: An integer representing how many words should be included (max: 15).
Here’s an example structure of the expected output in JSON format:

{{ matrix: [ ['C', 'A', 'T', 'E', 'R', 'P', 'I', 'L', 'L', 'A'], ['Q', 'U', 'A', 'C', 'K', 'D', 'O', 'G', 'S', 'F'], ['R', 'A', 'B', 'B', 'I', 'T', 'O', 'X', 'Y', 'Z'], ['T', 'H', 'E', 'E', 'L', 'O', 'T', 'A', 'C', 'H'], ['E', 'L', 'E', 'P', 'H', 'A', 'N', 'T', 'U', 'T'], ['M', 'O', 'U', 'S', 'E', 'R', 'F', 'R', 'O', 'G'], ['K', 'O', 'A', 'L', 'A', 'B', 'E', 'E', 'E', 'R'], ['F', 'I', 'S', 'H', 'L', 'E', 'O', 'T', 'H', 'E'], ['S', 'H', 'A', 'R', 'K', 'W', 'E', 'T', 'U', 'Y'], ['B', 'I', 'R', 'D', 'R', 'A', 'N', 'C', 'H', 'T'] ], words: ['CAT', 'DOG', 'RABBIT', 'QUACK', 'ELEPHANT', 'MOUSE', 'FROG', 'KOALA', 'SHARK', 'BIRD'], settings: {{ topic: "animals", wordLength: "medium", numberOfWords: 10 }} }};

Please ensure that the generated object is valid and meets all the specified requirements. Use these settings to create a game object in JSON format:

settings: {{ topic: {topic}, wordLength: {word_length}, numberOfWords: {number_of_words} }}"""
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
    app.run(host='0.0.0.0', port=5001)
    app.run(debug=True)



