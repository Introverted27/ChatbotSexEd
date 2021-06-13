from flask import Flask, render_template, request, jsonify
from rasa_nlu.model import Interpreter

# Python In-Built Packages
import os
import json
import random

interpreter = Interpreter.load('models/current/nlu')

app = Flask(__name__)
app.url_map.strict_slashes = False


def get_definition(keysearch):
    keysearch = keysearch.lower()
    file = './data/definitions.json'
    with open(file) as json_file:
        data = json.load(json_file)
        flagfound = False
        if keysearch in data.keys():
            result = data[keysearch]
        else:
            for key, value in data.items():
                if key.startswith(keysearch):  # Redundant, but keep it for now
                    result = key + " : " + value
                    flagfound = True
                    return result
                elif keysearch in key:
                    result = key + " : " + value
                    flagfound = True
                    return result
            if not flagfound:
                result = "Sorry, no information"
        return result


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/chat')
def chatbot():
    return render_template('chat0.html')


@app.route('/api/reply')
def msg_reply():
    message = request.args.get('q')
    content = interpreter.parse(message)
    intent = content['intent']['name']
    entities = content['entities']
    # 'greet': ['Hi', 'Hey', 'Hello', 'Hi there', 'Heya!']
    intent_replies = {
        'greet': [
            'hi there! I am here to answer your questions about sex. Tell me what you want to know?'
        ],
        'goodbye': ['Bye', 'See Ya!', 'Take Care'],
        'thanks': ['Always happy to help', 'You\'re welcome.', ':)']
    }
    if intent == 'query':
        if entities == None:
            reply = 'Sorry I don\'t understand.'
        else:
            keysearch = entities[0]['value']

            reply = get_definition(keysearch)
    elif intent in intent_replies.keys():
        reply = random.choice(intent_replies[intent])
    else:
        reply = 'Sorry I don\'t understand. Can you please repeat.'
    return jsonify(reply)


if __name__ == '__main__':
    # Development
    # app.run(host='127.0.0.1', port=5000, debug=True)

    # Production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
