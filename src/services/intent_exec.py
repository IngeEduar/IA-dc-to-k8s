from flask import jsonify

from src.actions.build import build_code
from src.nlp.recognizer.intent_recognizer import extract_intents
from src.nlp.spacy.extract import get_data_from_text
from src.actions.generic_actions import greet, not_found

FIELD_LABELS = {
    "kind":        "tipo de recurso",
    "name":        "nombre",
    "namespace":   "namespace",
    "image":       "imagen",
    "port":        "puerto",
    "labels":      "etiquetas",
    "configMap":   "configMap",
    "command":     "comando",
    "ingress":     "ingress",
    "volume":      "volumen",
}

def get_message(data: dict, intents: list, code: str) -> str:
    if data.get("return_yaml"):
        link = data.get("download_link", "https://example.com/")
        return f"Aquí está el enlace para descargar sus manifiestos: [Descargar]({link})"

    fragments = []
    for field, label in FIELD_LABELS.items():
        if field not in data:
            continue
        val = data[field]
        if not val:
            continue

        if isinstance(val, dict):
            val_str = ", ".join(f"{k}={v}" for k, v in val.items())
        elif isinstance(val, (list, tuple)):
            val_str = " ".join(str(x) for x in val)
        elif isinstance(val, bool):
            if not val:
                continue
            val_str = label  # ej. “ingress”
        else:
            val_str = str(val)

        fragments.append(f"{label} “{val_str}”")

    if data.get("resources"):
        res = data["resources"]
        if "limits" in res:
            lim = ", ".join(f"{k}={v}" for k, v in res["limits"].items())
            fragments.append(f"límites [{lim}]")
        if "requests" in res:
            req = ", ".join(f"{k}={v}" for k, v in res["requests"].items())
            fragments.append(f"peticiones [{req}]")

    if not fragments:
        base = "Hemos procesado su petición"
    else:
        base = "Hemos generado " + "; ".join(fragments)

    if intents:
        acciones = ", ".join(intents)
        base += f". Acciones detectadas: {acciones}"

    if code:
        base += f"\n```yaml\n{code}\n```"

    return base + "\nSi necesitas algo más, puedes decirmelo."

def intent_exec(user_text):
    intents = extract_intents(user_text)
    data = get_data_from_text(user_text)
    message = ""

    for intent in intents:
        if intent in globals() and callable(globals()[intent]):
            message = globals()[intent]()
        else:
            code = build_code(intents, data)
            message = get_message(data, intents, code)

    json_response = {"message": message, "actions": intents}

    return jsonify(json_response), 200