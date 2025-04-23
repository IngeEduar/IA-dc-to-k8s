DATA = [
    {
        "image": "postgres",
        "name": "Postgres",
        "tags": [
            "14",
            "latest"
        ],
        "environments": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "",
            "POSTGRES_DB": "database"
        },
        "kind": "StatefulSet",
        "ports": [
            "5432"
        ],
        "volumes": {
            "/var/lib/postgresql": "10Gi",
            "/backups": "5Gi"
        },
        "labels": {
            "app": "postgres"
        },
        "service_type": "ClusterIP",
        "ingress": False,
        "replicas": 1,
        "resources": {
            "requests": {
                "memory": "2Gi",
                "CPU": "1000m"
            },
            "limits": {
                "memory": "2Gi",
                "CPU": "1000m"
            }
        },
        "comment": "Estos son los manifiestos para tu servicio de postgres"
    }
]


def get_service_data(service):
    for service_data in DATA:
        if service["image"] == service_data["image"]:
            service_data["tags"] = "latest"
            return service_data

    return  {}

def generate_new_service_data(service_name, service):
    image_data = service.get("image", "")
    if ":" in image_data:
        image, tag = image_data.split(":")
    else:
        image, tag = image_data, "latest"

    return {
        "image": image,
        "name": service_name,
        "tags": tag,
        "environments": service.get("environment", {}),
        "kind": "StatefulSet" if "database" in service.get("name", "").lower() else "Deployment",  # Detecta si es un servicio de BD
        "ports": [port.split(":")[1] for port in service.get("ports", [])] if service.get("ports") else [],
        "volumes": {volume_dir.split(":")[1]: "5Gi" for volume_dir in service.get("volumes", {})},
        "labels": service.get("labels", {}),
        "service_type": service.get("service_type", "ClusterIP"),
        "ingress": service.get("ingress", False),
        "replicas": service.get("deploy", {}).get("replicas", 1),
        "resources": service.get("resources", {}),
        "comment": service.get("comment", "")
    }
