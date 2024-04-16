from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

@app.route('/generate-response', methods=['POST'])
def generate_response():
    data = request.json
    messages = data.get('messages', [])
    user_message = messages[-1]['content']  # Assuming user message is the last message
    
    # Call OpenAI API to generate response
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful email assistant for Josh and you will be responding as Josh. You will be drafting email responses for users based on given message in their inbox. If you do not know how to respond you will ask for more guidance."},
            {"role": "user", "content": user_message}  # Pass user message to the API
        ]
    )
    
    # Extract generated response from completion
    response = completion['choices'][0]['message']['content']
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
