import os
import numpy as np
import keras.models
import speech_recognition as sr
import transformers
import threading
from utils import wake_up, action_time, calculate_emotion_percentages, calculate_stress_level
from record_analysis import record_and_analyze_user_input
from text_to_speech import text_to_speech

loaded_model = keras.models.load_model('C:/Users/malithg/PycharmProjects/AI_Virtual_C/my_model.h5')

classLabels = ('Angry', 'Fear', 'Disgust', 'Happy', 'Sad', 'Surprised', 'Neutral')

conversation = []  # Initialize an empty list to store the conversation

class ChatBot:
    def __init__(self, name):
        self.res = None
        self.text = None
        print("----- Starting up", name, "-----")
        self.name = name
        self.user_input_counter = 0
        self.user_inputs = []
        self.sentiment_analysis = []
        self.record_thread = None

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        sr.Microphone()

        with sr.Microphone() as mic:
            print("Listening...")
            try:
                audio = recognizer.listen(mic)
                self.text = recognizer.recognize_google(audio)
                print("Me  -->", self.text)
            except sr.UnknownValueError:
                print("Me  --> Could not understand audio")
            except sr.RequestError as e:
                print(f"Me  --> Speech recognition request failed: {e}")
            except Exception as e:
                print(f"Me  --> An error occurred: {e}")

    def run(self):

        nlp = transformers.pipeline("conversational", model="microsoft/DialoGPT-medium")
        tokenizer = nlp.tokenizer
        tokenizer.padding_side = "left"  # Set padding side to left
        os.environ["TOKENIZERS_PARALLELISM"] = "true"

        # Initial AI response
        initial_response = "Hello, I am AI Counselor. How is the day?"
        #conversation.append({'AI': initial_response})  # Add to conversation list
        conversation.append('AI: ' + initial_response)

        text_to_speech(initial_response)

        while True:
            self.speech_to_text()


            if self.text:
                print(f'User Input: {self.text}')
                #conversation.append({'User': self.text})
                conversation.append('User: ' + self.text)

            if wake_up(self.text, self.name):
                self.res = "Hello, I am an AI counselor. How is the Day?"
            elif "time" in self.text:
                self.res = action_time()
            elif any(i in self.text for i in ["thank", "thanks"]):
                self.res = np.random.choice(
                    ["You're welcome!", "Anytime!", "No problem!", "Cool!", "I'm here if you need me!",
                     "You're welcome!"]
                )
            elif any(i in self.text for i in ["exit", "close"]):
                self.res = np.random.choice(
                    ["Tata", "Have a good day", "Bye", "Goodbye", "Hope to meet soon", "Peace out!"]
                )
                text_to_speech(self.res)
                break
            else:
                if self.text == "ERROR":
                    self.res = "Sorry, come again?"
                else:
                    if self.record_thread and self.record_thread.is_alive():
                        self.record_thread.join()  # Wait for the previous thread to finish if it's still running

                    # Start a new thread to run record_and_analyze_user_input()
                    self.record_thread = threading.Thread(target=record_and_analyze_user_input, args=(self,))
                    self.record_thread.start()

                    chat = nlp(transformers.Conversation(self.text), pad_token_id=50256)
                    self.res = str(chat)
                    self.res = self.res[self.res.find("bot >> ") + 7:].strip()

                # Store the conversation in a list
                #conversation.append({'AI': self.res})
                conversation.append('AI: ' + self.res)

                # Print the AI response immediately if it was added to the conversation
                if self.res:
                    print(f'AI Response: {self.res}')

            text_to_speech(self.res)

        overall_emotion = self.sentiment_analysis
        stress_level = calculate_stress_level(self.sentiment_analysis)
        print("Overall Emotion of the conversation:", overall_emotion)
        print("stress level:", stress_level)
        print("Conversation:", conversation)

        # Print the last AI response after the conversation ends if it was added to the conversation
        if self.res:
            print(f'AI Response: {self.res}')

        print("----- Closing down Dev -----")

if __name__ == "__main__":
    chatbot = ChatBot("AI Counselor")
    chatbot.run()
