import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

# Cargar ejemplos desde un JSON (con más variaciones)
training_data = [
    {"text": "Quiero MongoDB", "intent": "generate_mongodb"},
    {"text": "mongodb", "intent": "generate_mongodb"},
    {"text": "MongoDB", "intent": "generate_mongodb"},
    {"text": "Necesito una base de datos en Mongo", "intent": "generate_mongodb"},
    {"text": "Añadir MongoDB a la configuración", "intent": "generate_mongodb"},
    {"text": "Instalar Redis para cache", "intent": "generate_redis"},
    {"text": "Usar Redis en mi aplicación", "intent": "generate_redis"},
    {"text": "Habilitar cache con Redis", "intent": "generate_redis"},
    {"text": "Escalar con Kubernetes", "intent": "scale_replicas"},
    {"text": "Necesito más réplicas", "intent": "scale_replicas"},
    {"text": "Aumentar las instancias en Kubernetes", "intent": "scale_replicas"},
    {"text": "Genera un archivo YAML", "intent": "generate_yaml"},
    {"text": "Necesito un YAML de configuración", "intent": "generate_yaml"},
    {"text": "Crear un manifiesto YAML", "intent": "generate_yaml"},
]

X_train = [item["text"] for item in training_data]
y_train = [item["intent"] for item in training_data]

# Vectorizar texto
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

# Modelo de clasificación multietiqueta
model = OneVsRestClassifier(LogisticRegression())
model.fit(X_train_tfidf, y_train)

# Guardar modelo y vectorizador
joblib.dump(model, "nlp/model.pkl")
joblib.dump(vectorizer, "nlp/vectorizer.pkl")

print("✅ Modelo entrenado y guardado")
