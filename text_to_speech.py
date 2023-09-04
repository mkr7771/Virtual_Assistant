import pyttsx3
from flask import jsonify


def text_to_speech(text):

    print("Dev -->", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

    # Send the conversation data to the front-end using jsonify (Flask)
    jsonify({'message': text})
