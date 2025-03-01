import joblib
from get_data import get_data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

training_data = get_data()

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
