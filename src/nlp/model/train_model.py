import joblib
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier

training_data = [
    {"texts": ["Hola, ¿cómo estás?","Hello","Hi","¡Hola!","Buenas","Hey","Saludos","Qué tal","Hola, buen día","Hola, ¿qué tal?","Hola, ¿cómo va?","Hola, un gusto saludarte","¡Hey! ¿Cómo andas?","Hola, ¿todo bien?","Hi there!","Hello, how are you?","Hola, ¿qué hay de nuevo?","Buenas, ¿cómo va?","¡Hey! ¿Qué pasa?","Hola, ¿cómo te encuentras?"], "intent": "greet"},
    {"texts": [
        "Quiero MongoDB", "mongodb", "MongoDB", "Necesito una base de datos en Mongo",
        "Añadir MongoDB a la configuración", "Crear un servicio de MongoDB en Kubernetes",
        "Desplegar MongoDB en mi clúster", "Generar un manifiesto para MongoDB",
        "Configurar una base de datos MongoDB", "Quiero una base de datos NoSQL como MongoDB",
        "Añadir una instancia de MongoDB", "Configurar almacenamiento persistente para MongoDB",
        "Necesito MongoDB en Kubernetes", "Cómo crear una base de datos en MongoDB",
        "Implementar MongoDB con persistencia", "Genera una configuración para MongoDB",
        "Quiero usar MongoDB con un volumen persistente", "Crear un StatefulSet para MongoDB",
        "Configurar autenticación en MongoDB", "Añadir un servicio de MongoDB con ClusterIP",
        "Generar mongodb", "para desplegar mongodb", "desplegar mongodb", "usando mongodb"
    ], "intent": "generate_mongodb"},

    # Redis
    {"texts": [
        "Instalar Redis para cache", "Usar Redis en mi aplicación", "Habilitar cache con Redis",
        "Quiero Redis en Kubernetes", "Añadir Redis como caché", "Cómo configurar Redis en un clúster",
        "Crear un servicio de Redis", "Configurar persistencia en Redis", "Necesito una caché en Redis",
        "Desplegar Redis en mi infraestructura", "Implementar un servidor Redis", "Configurar Redis con Kubernetes",
        "Genera un manifiesto YAML para Redis", "Cómo escalar Redis en Kubernetes",
        "Quiero usar Redis como base de datos",
        "Crear un StatefulSet para Redis", "Configurar Redis con alta disponibilidad",
        "Añadir un servicio de Redis con ClusterIP",
        "Configurar Redis con una contraseña segura", "Implementar Redis con almacenamiento persistente"
    ], "intent": "generate_redis"},

    # PostgreSQL
    {"texts": [
        "Necesito PostgreSQL", "Instalar PostgreSQL en Kubernetes", "Quiero una base de datos PostgreSQL",
        "Configurar PostgreSQL con almacenamiento persistente", "Añadir PostgreSQL al clúster",
        "Generar un manifiesto para PostgreSQL", "Configurar PostgreSQL con autenticación",
        "Quiero usar PostgreSQL en Kubernetes",
        "Crear un StatefulSet para PostgreSQL", "Implementar PostgreSQL con una base de datos inicial",
        "Cómo desplegar PostgreSQL en Kubernetes", "Configurar PostgreSQL con un volumen persistente",
        "Crear un servicio para PostgreSQL", "Configurar réplicas en PostgreSQL",
        "Cómo conectar mi aplicación a PostgreSQL",
        "Añadir PostgreSQL con almacenamiento en disco", "Configurar PostgreSQL con un usuario y contraseña",
        "Quiero una base de datos relacional como PostgreSQL", "Desplegar PostgreSQL con ClusterIP",
        "Crear un servicio PostgreSQL accesible desde mi aplicación"
    ], "intent": "generate_postgresql"},

    # MySQL
    {"texts": [
        "Necesito MySQL", "Instalar MySQL en Kubernetes", "Cómo crear una base de datos MySQL",
        "Añadir MySQL a mi clúster", "Quiero un servicio MySQL", "Cómo desplegar MySQL en Kubernetes",
        "Generar un manifiesto para MySQL", "Configurar almacenamiento persistente en MySQL",
        "Configurar MySQL con usuario y contraseña", "Crear un StatefulSet para MySQL",
        "Desplegar MySQL en mi infraestructura", "Cómo conectar MySQL a mi aplicación",
        "Quiero usar MySQL en Kubernetes", "Configurar MySQL con un volumen persistente",
        "Añadir MySQL con ClusterIP", "Configurar una base de datos inicial en MySQL",
        "Implementar MySQL con réplicas", "Cómo gestionar MySQL en un clúster Kubernetes",
        "Crear un servicio de MySQL accesible desde mi aplicación", "Configurar MySQL con backups automáticos"
    ], "intent": "generate_mysql"},

    # Elasticsearch
    {"texts": [
        "Necesito Elasticsearch", "Quiero un clúster de Elasticsearch", "Instalar Elasticsearch en Kubernetes",
        "Cómo desplegar Elasticsearch", "Configurar almacenamiento en Elasticsearch",
        "Crear un StatefulSet para Elasticsearch", "Añadir Elasticsearch a mi infraestructura",
        "Generar un manifiesto YAML para Elasticsearch", "Configurar Elasticsearch con seguridad",
        "Implementar Elasticsearch con persistencia", "Cómo escalar Elasticsearch en Kubernetes",
        "Configurar Elasticsearch con índices automáticos", "Añadir un servicio para Elasticsearch",
        "Configurar Elasticsearch con Logstash y Kibana", "Cómo conectar Elasticsearch a mi aplicación",
        "Configurar Elasticsearch con volúmenes persistentes", "Quiero un servicio de Elasticsearch accesible",
        "Añadir un clúster de Elasticsearch con alta disponibilidad", "Configurar Elasticsearch con réplicas",
        "Crear un servicio de Elasticsearch con ClusterIP"
    ], "intent": "generate_elasticsearch"},

    # Nginx
    {"texts": [
        "Necesito un servidor Nginx", "Instalar Nginx en Kubernetes", "Quiero usar Nginx como proxy",
        "Configurar Nginx en un clúster Kubernetes", "Cómo desplegar Nginx en Kubernetes",
        "Generar un manifiesto YAML para Nginx", "Añadir Nginx como balanceador de carga",
        "Configurar Nginx con reglas de enrutamiento", "Cómo hacer un Ingress con Nginx",
        "Implementar Nginx con configuración personalizada", "Crear un servicio Nginx en Kubernetes",
        "Configurar Nginx con HTTPS", "Cómo hacer redirecciones en Nginx",
        "Añadir Nginx con almacenamiento persistente",
        "Configurar Nginx con un archivo de configuración externo", "Quiero un servicio de Nginx con ClusterIP",
        "Implementar un Nginx como proxy inverso", "Configurar Nginx con módulos personalizados",
        "Desplegar Nginx con múltiples sitios virtuales", "Crear un servicio para Nginx accesible desde el clúster"
    ], "intent": "generate_nginx"},

    # Generación de archivos YAML
    {"texts": [
        "Genera un archivo YAML", "Necesito un YAML de configuración", "Crear un manifiesto YAML",
        "Cómo hacer un YAML para Kubernetes", "Generar configuración en YAML",
        "Crear un Deployment en YAML", "Quiero un archivo YAML para un servicio",
        "Cómo escribir un manifiesto YAML", "Generar un YAML para un Ingress",
        "Quiero crear un ConfigMap en YAML", "Generar un YAML para un Secret",
        "Crear un Service en YAML", "Cómo escribir un YAML para un StatefulSet",
        "Crear un DaemonSet en YAML", "Generar un YAML para una aplicación",
        "Cómo definir volúmenes en un YAML", "Quiero un YAML para una base de datos",
        "Cómo configurar variables de entorno en YAML", "Generar un YAML para un CronJob",
        "Quiero un YAML con múltiples recursos de Kubernetes"
    ], "intent": "generate_yaml"}
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
