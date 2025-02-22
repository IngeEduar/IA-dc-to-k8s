from flask import Blueprint, request, jsonify, send_from_directory
from nlp.intent_recognizer import extract_intents
from k8s_generator.manifest_builder import generate_k8s_manifest
import os, uuid

main_bp = Blueprint("main", __name__)

TMP_DIR = "tmp"

@main_bp.route("/convert", methods=["POST"])
def convert_request():
    user_text = request.form.get("message", "")
    docker_compose_file = request.files.get("file")

    if not docker_compose_file:
        return jsonify({"error": "Debe incluir un archivo docker-compose.yml"}), 400

    intent = extract_intents(user_text)[0]
    manifest_yaml = generate_k8s_manifest(intent, docker_compose_file)

    file_route = f"{uuid.uuid4()}-{intent}.yaml"
    file_path = f"{TMP_DIR}/{file_route}"
    with open(file_path, "w") as file:
        file.write(manifest_yaml)

    return jsonify({
        "message": "Aquí está su archivo",
        "url": f"{request.host_url}download/{file_route}"
    })

@main_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    file_path = f"{TMP_DIR}/{filename}"
    if os.path.exists(file_path):
        return send_from_directory(TMP_DIR, filename, as_attachment=True)
    return jsonify({"error": "Archivo no encontrado"}), 404
