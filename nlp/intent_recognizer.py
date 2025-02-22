import joblib

# Cargar el modelo entrenado
model = joblib.load("nlp/model.pkl")
vectorizer = joblib.load("nlp/vectorizer.pkl")

def extract_intent(user_text):
    """Usa IA para predecir la intención del usuario"""
    user_input_tfidf = vectorizer.transform([user_text])
    prediction = model.predict(user_input_tfidf)[0]
    return prediction
