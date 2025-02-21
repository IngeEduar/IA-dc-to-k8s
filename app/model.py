import yaml
import os
from io import StringIO

DEFAULT_DB_PORTS = {
    "postgres": 5432,  # puerto por defecto
    "mysql": 3306,  # puerto por defecto
}

TMP_DIR = "/tmp"


def process_message(user_text, docker_compose_file):
    try:
        # Leer el archivo docker-compose
        docker_compose_data = yaml.safe_load(docker_compose_file.read())

        # Verificar si el archivo tiene servicios
        if "services" not in docker_compose_data:
            return {"error": "El archivo docker-compose no contiene servicios válidos."}

        services = docker_compose_data["services"]
        kubernetes_configs = []

        # Lógica para procesar servicios según el texto del usuario
        if "base de datos" in user_text.lower():
            # Filtrar servicios que puedan ser bases de datos
            db_services = [
                service_name
                for service_name, service_data in services.items()
                if "postgres" in service_data.get("image", "").lower()
                   or "mysql" in service_data.get("image", "").lower()
            ]

            if len(db_services) > 1:
                return {
                    "error": f"Se detectaron múltiples bases de datos: {', '.join(db_services)}. Especifique cuál desea pasar."}

            # Generar StatefulSet para bases de datos
            for db_service in db_services:
                kubernetes_configs.append(generate_statefulset(db_service, services[db_service]))

        else:
            # Si no especifica, pasar todos los servicios a Kubernetes
            for service_name, service_data in services.items():
                if "postgres" in service_data.get("image", "").lower():
                    kubernetes_configs.append(generate_statefulset(service_name, service_data))
                else:
                    kubernetes_configs.append(generate_deployment(service_name, service_data))

        # Si el usuario solicita un archivo YAML
        if "devuelve un archivo yaml" in user_text.lower():
            yaml_filename = save_yaml_file(kubernetes_configs)
            download_url = f"http://127.0.0.1:5000/download/{yaml_filename}"
            return {
                "message": "Aquí está su archivo",
                "url": download_url,
            }

        return {"kubernetes_configs": kubernetes_configs}

    except yaml.YAMLError as e:
        return {"error": f"Error al procesar el archivo YAML: {str(e)}"}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}


def generate_statefulset(service_name, service_data):
    # Verificar el puerto para bases de datos conocidas
    image = service_data.get("image", "").lower()
    port = "<su puerto aquí>"

    for db_name, default_port in DEFAULT_DB_PORTS.items():
        if db_name in image:
            port = f"{default_port}"
            break

    return {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {"name": service_name},
        "spec": {
            "selector": {"matchLabels": {"app": service_name}},
            "serviceName": service_name,
            "replicas": 1,
            "template": {
                "metadata": {"labels": {"app": service_name}},
                "spec": {
                    "containers": [
                        {
                            "name": service_name,
                            "image": service_data["image"],
                            "ports": [{"containerPort": port}],
                        }
                    ]
                },
            },
        },
    }


def generate_deployment(service_name, service_data):
    # Verificar el puerto para servicios no persistentes
    ports = service_data.get("ports", [80])
    port = ports[0] if ports else "su puerto aquí"

    return {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": service_name},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"app": service_name}},
            "template": {
                "metadata": {"labels": {"app": service_name}},
                "spec": {
                    "containers": [
                        {
                            "name": service_name,
                            "image": service_data["image"],
                            "ports": [{"containerPort": port}],
                        }
                    ]
                },
            },
        },
    }


def save_yaml_file(kubernetes_configs):
    # Guardar todos los manifiestos YAML en un único archivo
    yaml_filename = "kubernetes_manifests.yaml"
    yaml_path = os.path.join(TMP_DIR, yaml_filename)

    with open(yaml_path, "w") as yaml_file:
        for config in kubernetes_configs:
            yaml.dump(config, yaml_file, sort_keys=False)
            yaml_file.write("---\n")

    return yaml_filename

