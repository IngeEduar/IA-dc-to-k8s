import yaml

DEFAULT_PORTS = {
    "mongodb": 27017,  # Puerto por defecto
    "redis": 6379,
    "postgres": 5432,
}

def generate_k8s_manifest(docker_compose_file):
    docker_compose_data = yaml.safe_load(docker_compose_file.read())

    if "services" not in docker_compose_data:
        return {"error": "El archivo docker-compose no contiene servicios válidos."}

    services = docker_compose_data["services"]
    manifests = []

    for service_name, service_data in services.items():
        is_db = any(db in service_data.get("image", "").lower() for db in DEFAULT_PORTS.keys())

        # Definir puerto
        port = service_data.get("ports", [None])[0]
        if is_db:
            if port is None:
                port = f"<su puerto aquí>"
            else:
                db_type = next((db for db in DEFAULT_PORTS if db in service_data["image"]), None)
                if db_type:
                    port = f"{port}"

        # Crear manifest
        manifests.append({
            "apiVersion": "apps/v1",
            "kind": "StatefulSet" if is_db else "Deployment",
            "metadata": {"name": service_name},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"app": service_name}},
                "template": {
                    "metadata": {"labels": {"app": service_name}},
                    "spec": {
                        "containers": [{
                            "name": service_name,
                            "image": service_data["image"],
                            "ports": [{"containerPort": port}],
                        }]
                    },
                },
            },
        })

    return yaml.dump_all(manifests, default_flow_style=False)
