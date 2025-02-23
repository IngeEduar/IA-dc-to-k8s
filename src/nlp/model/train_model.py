import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

training_data = [
    {"texts": ["Quiero MongoDB", "mongodb", "MongoDB", "Necesito una base de datos en Mongo", "Añadir MongoDB a la configuración"], "intent": "generate_mongodb"},
    {"texts": ["Instalar Redis para cache", "Usar Redis en mi aplicación", "Habilitar cache con Redis"], "intent": "generate_redis"},
    {"texts": ["Escalar con Kubernetes", "Necesito más réplicas", "Aumentar las instancias en Kubernetes"], "intent": "scale_replicas"},
    {"texts": ["Genera un archivo YAML", "Necesito un YAML de configuración", "Crear un manifiesto YAML"], "intent": "generate_yaml"},
    {"texts": ["Hola, ¿cómo estás?","Hello","Hi","¡Hola!","Buenas","Hey","Saludos","Qué tal","Hola, buen día","Hola, ¿qué tal?","Hola, ¿cómo va?","Hola, un gusto saludarte","¡Hey! ¿Cómo andas?","Hola, ¿todo bien?","Hi there!","Hello, how are you?","Hola, ¿qué hay de nuevo?","Buenas, ¿cómo va?","¡Hey! ¿Qué pasa?","Hola, ¿cómo te encuentras?"], "intent": "greet"}
]

# Expandir datos en listas planas
X_train = []
y_train = []
for item in training_data:
    X_train.extend(item["texts"])  # Agregar todas las variaciones
    y_train.extend([item["intent"]] * len(item["texts"]))  # Repetir la intención

# Vectorizar texto
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)

# Modelo de clasificación
model = OneVsRestClassifier(LogisticRegression())
model.fit(X_train_tfidf, y_train)

# Guardar modelo y vectorizador
joblib.dump(model, "src/nlp/model/model.pkl")
joblib.dump(vectorizer, "src/nlp/model/vectorizer.pkl")

print("✅ Modelo entrenado y guardado con frases agrupadas por intención")
