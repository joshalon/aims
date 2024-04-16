from flask import Flask, request, jsonify
from openai import OpenAI
import logging
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")

app = Flask(__name__)
client = OpenAI()
app.logger.setLevel(logging.DEBUG)

@app.route('/generate-response', methods=['POST'])
def generate_response():
    app.logger.info('This is a log message')
    data = request.json
    app.logger.debug("Received data: %s", data)
    messages = data.get('messages', [])
    user_message = messages[-1]['content']

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful email assistant for Josh and you will be responding as Josh. You will be drafting email responses for users based on given message in their inbox. If you do not know how to respond you will ask for more guidance."},
            {"role": "user", "content": user_message}
        ]
    )

    response = completion.choices[0].message.content
    app.logger.info(response)
    return response

if __name__ == '__main__':
    app.run(debug=True)