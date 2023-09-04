import pyttsx3
import os

def text_to_speech(text):
    print("Dev -->", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


    # Update the conversation output on the webpage
    js_command = f"updateConversation('{text}')"
 #   os.system(f"node -e '{js_command}'")  # Run Node.js command
