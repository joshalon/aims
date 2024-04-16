from flask import Flask, request
from openai import OpenAI
import logging
import os

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

@app.route("/", methods=['POST'])
def generate_response():
    app.logger.info('This is a log message')
    data = request.get_json()
    app.logger.debug("Received data: %s", data)

    if 'messages' not in data or not isinstance(data['messages'], list):
        app.logger.error("Invalid request data: %s", data)
        return "Invalid request data", 400

    messages = data['messages']
    if not all('role' in msg and 'content' in msg for msg in messages):
        app.logger.error("Invalid request data: %s", data)
        return "Invalid request data", 400

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful email assistant for Josh and you will be responding as Josh. You will be drafting email responses for users based on given message in their inbox. If you do not know how to respond you will ask for more guidance."},
                *messages
            ]
        )
        response = completion.choices[0].message.content
        app.logger.info(response)
        return response
    except Exception as e:
        app.logger.error("Error calling OpenAI API: %s", str(e))
        return "Error calling OpenAI API", 500