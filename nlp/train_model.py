import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Cargar ejemplos desde un JSON
training_data = [
    {"text": "Quiero MongoDB", "intent": "mongodb"},
    {"text": "Necesito Redis para cache", "intent": "redis"},
    {"text": "Escalar con Kubernetes", "intent": "replicas"},
    {"text": "Genera un archivo YAML", "intent": "archivo"},
]

X_train = [item["text"] for item in training_data]
y_train = [item["intent"] for item in training_data]

# Vectorizar texto
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

# Modelo de clasificación
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Guardar modelo
joblib.dump(model, "nlp/model.pkl")
joblib.dump(vectorizer, "nlp/vectorizer.pkl")

print("✅ Modelo entrenado y guardado")
