import joblib
import numpy as np

from src.services.spam_detector.spam_detector import spam_detector

model = joblib.load("src/nlp/model/model.pkl")
vectorizer = joblib.load("src/nlp/model/vectorizer.pkl")

def extract_intents(user_text, threshold=0.7):
    if spam_detector(user_text):
        return ["spam"]

    user_input_tfidf = vectorizer.transform([user_text])
    probabilities = model.predict_proba(user_input_tfidf)[0]

    # print(f"Probabilidades del modelo: {probabilities}") DEBUG

    intent_list = model.classes_

    detected_intents = [str(intent_list[i]) for i in np.where(probabilities >= threshold)[0]]

    while not detected_intents:
        threshold -= 0.1
        detected_intents = [str(intent_list[i]) for i in np.where(probabilities >= threshold)[0]]

        if threshold == 0.3:
            detected_intents = ["not_found"]
#        max_prob_index = np.argmax(probabilities) Take first item
#        detected_intents.append(str(intent_list[max_prob_index]))


    return detected_intents

## DEBUG
#text = "Quiero MongoDB y Usar Redis en mi aplicación"
#print(f"Intenciones detectadas: {extract_intents(text)}")
