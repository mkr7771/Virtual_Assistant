import datetime

def wake_up(text, name):
    return True if name in text.lower() else False

def action_time():
    return datetime.datetime.now().time().strftime('%H:%M')

def calculate_stress_level(sentiment_analysis):
    # Determine stress level based on detected emotions
    if any(emotion in sentiment_analysis for emotion in ["Angry", "Fear", "Sad", "Disgust"]):
        return "High Stress"
    elif any(emotion in sentiment_analysis for emotion in ["Happy", "Disgust"]):
        return "Low Stress"
    else:
        return "Low Stress"

def calculate_emotion_percentages(sentiment_analysis):
    total_emotions = len(sentiment_analysis)
    emotion_count = {}
    for emotion in sentiment_analysis:
        emotion_count[emotion] = emotion_count.get(emotion, 0) + 1
    emotion_percentages = {}
    for emotion, count in emotion_count.items():
        percentage = (count / total_emotions) * 100
        emotion_percentages[emotion] = round(percentage, 2)
    return emotion_percentages