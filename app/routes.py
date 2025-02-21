from flask import Blueprint, request, jsonify, send_from_directory
from .model import process_message, TMP_DIR

main_bp = Blueprint("main", __name__)

@main_bp.route("/message/", methods=["POST"])
def handle_message():
    docker_compose_file = request.files.get("file")
    user_text = request.form.get("text", "")

    if not docker_compose_file:
        return jsonify({"error": "Debe incluir un archivo docker-compose.yml"}), 400

    if not user_text:
        user_text = ""

    response = process_message(user_text, docker_compose_file)

    return jsonify(response)


@main_bp.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    # Ruta para descargar el archivo YAML
    return send_from_directory(TMP_DIR, filename, as_attachment=True)