import joblib
import numpy as np

model = joblib.load("nlp/model.pkl")
vectorizer = joblib.load("nlp/vectorizer.pkl")

def extract_intents(user_text, threshold=0.2):
    user_input_tfidf = vectorizer.transform([user_text])
    probabilities = model.predict_proba(user_input_tfidf)[0]

    # print(f"Probabilidades del modelo: {probabilities}") DEBUG

    intent_list = model.classes_

    detected_intents = [str(intent_list[i]) for i in np.where(probabilities >= threshold)[0]]

    if not detected_intents:
        max_prob_index = np.argmax(probabilities)
        detected_intents.append(str(intent_list[max_prob_index]))

    return detected_intents

## DEBUG
#text = "Quiero MongoDB y Usar Redis en mi aplicación"
#print(f"Intenciones detectadas: {extract_intents(text)}")
