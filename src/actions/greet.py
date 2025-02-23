import random

def greet():
    greets = [
        "Hola, ¿cómo estás? ¿puedo ayudarte?",
        "¡Hola! Me siento afortunado de tenerte aquí.",
        "Hola, ¿puedo ayudarte creando manifiestos de Kubernetes?",
        "¡Hola! ¿En qué puedo asistirte hoy?",
        "¡Hey! Qué bueno verte por aquí.",
        "Hola, listo para resolver cualquier duda que tengas.",
        "¡Hola! ¿Listo para desplegar algo genial en Kubernetes?",
        "Bienvenido, dime en qué puedo ayudarte hoy.",
        "¡Hola! Kubernetes y yo estamos listos para trabajar contigo.",
        "Saludos, ¿qué desafío técnico enfrentamos hoy?",
        "¡Hey! Siempre es buen momento para aprender algo nuevo.",
        "Hola, el clúster está esperando instrucciones. ¿Qué hacemos?",
        "¡Bienvenido! Estoy listo para ayudarte con cualquier consulta.",
        "Hola, ¿todo bien? Cuéntame cómo puedo ser útil.",
        "¡Saludos! Listo para desplegar conocimiento.",
        "Hola, dime qué necesitas y lo resolveremos juntos.",
        "¡Ey! Kubernetes no duerme y yo tampoco. ¿En qué te ayudo?",
        "Hola, ¿listo para optimizar tus despliegues?",
        "¡Hey! Despleguemos algo interesante hoy.",
        "Hola, el YAML no se escribirá solo. ¿Comenzamos?",
        "¡Saludos! Kubernetes y Python están listos para la acción.",
        "Hola, dime qué necesitas y lo configuramos en un instante.",
        "¡Bienvenido! Aquí para hacer que tus contenedores cobren vida.",
    ]
    return random.choice(greets)
