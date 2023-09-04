import sys
import os
import sounddevice as sd
import numpy as np
import librosa
import keras.models

# Load the saved emotion identification model
loaded_model = keras.models.load_model('C:/Users/malithg/PycharmProjects/AI_Virtual_C/my_model.h5')
classLabels = ('Angry', 'Fear', 'Disgust', 'Happy', 'Sad', 'Surprised', 'Neutral')

def record_and_analyze_user_input(chatbot):
    duration = 2.5  # Set the duration of the recording (in seconds)
    sample_rate = 22050 * 2  # Set the sample rate of the recording

    # Redirect standard output to a null device
    sys.stdout = open(os.devnull, 'w')

    # Record the live audio
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until the recording is finished

    # Restore standard output
    sys.stdout = sys.__stdout__

    # Preprocess the recorded audio
    mfccs = librosa.feature.mfcc(y=recording.flatten(), sr=sample_rate, n_mfcc=39)
    input_data = mfccs[np.newaxis, ..., np.newaxis]

    # Perform emotion prediction
    with np.printoptions(suppress=True):
        predictions = loaded_model.predict(input_data)

    # Get the predicted label
    predicted_label = classLabels[np.argmax(predictions)]

    # Store the predicted emotion in the array
    chatbot.sentiment_analysis.append(predicted_label)

    return predicted_label