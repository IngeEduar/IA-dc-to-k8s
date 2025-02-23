from flask import Blueprint, request, jsonify, send_from_directory
from src.nlp.recognizer.intent_recognizer import extract_intents
from src.services.manifest_builder import generate_k8s_manifest_docker_compose
from src.actions.greet import greet
import os, uuid

main_bp = Blueprint("main", __name__)

TMP_DIR = "tmp"

@main_bp.route("/convert", methods=["POST"])
def convert_request():
    user_text = request.form.get("message", "")
    docker_compose_file = request.files.get("file")

    if bool(user_text) == bool(docker_compose_file):
        return jsonify({"error": "Debe enviar solo texto o solo un archivo, no ambos."}), 400

    if not bool(user_text) and not bool(docker_compose_file):
        return jsonify({"error": "Debe enviar un texto o un archivo docker compose."}), 400

    if docker_compose_file:
        manifest_yaml = generate_k8s_manifest_docker_compose(docker_compose_file)

        file_route = f"{uuid.uuid4()}.yaml"
        file_path = f"{TMP_DIR}/{file_route}"
        with open(file_path, "w") as file:
            file.write(manifest_yaml)

        return jsonify({
            "message": "Aquí está su archivo",
            "url": f"{request.host_url}download/{file_route}",
        })

    intents = extract_intents(user_text)

    json_response = {
        "message": "Estas son sus acciones",
        "actions": intents
    }

    for intent in intents:
        if intent in globals() and callable(globals()[intent]):
            output = globals()[intent]()
            json_response[intent] = output

    return jsonify(json_response)

@main_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = f"{TMP_DIR}/{filename}"
    if os.path.exists(file_path):
        return send_from_directory(TMP_DIR, filename, as_attachment=True)
    return jsonify({"error": "Archivo no encontrado"}), 404
