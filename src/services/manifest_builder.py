import yaml

DATA = [
    {
        "image": "postgres",
        "name": "postgres",
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


def merge_services(service_stored, service_data):
    merged_service = service_stored.copy()  # Copia para no modificar el original

    for key, value in service_data.items():
        if isinstance(value, dict):
            merged_service[key] = merge_services(service_stored.get(key, {}), value)
        elif isinstance(value, list):
            merged_service[key] = value if value else service_stored.get(key, [])
        else:
            merged_service[key] = value if value is not None else service_stored.get(key, "")

    return merged_service


def generate_k8s_manifest_docker_compose(docker_compose_file):
    docker_compose_data = yaml.safe_load(docker_compose_file.read())

    if "services" not in docker_compose_data:
        return {"error": "El archivo docker-compose no contiene servicios válidos."}

    services = docker_compose_data["services"]
    manifests = []

    for service_name, service_data in services.items():
        service_saved = get_service_data(service_data)
        service_generated = generate_new_service_data(service_name, service_data)

        service_stored = merge_services(service_saved, service_generated)

        ## Deployment
        manifests.append({
            "apiVersion": "apps/v1",
            "kind": service_stored["kind"],
            "metadata": {
                "name": service_stored["name"],
                ** ({"labels": service_stored["labels"]} if "labels" in service_stored and service_stored["labels"] else {})
            },
            "spec": {
                "restartPolicy": "Always",
                "replicas": service_stored["replicas"],
                "selector": {
                    "matchLabels": {
                        "app": service_stored["name"],
                        ** ({"labels": service_stored["labels"]} if "labels" in service_stored and service_stored["labels"] else {})
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": service_stored["name"],
                            ** ({"labels": service_stored["labels"]} if "labels" in service_stored and service_stored["labels"] else {})
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": service_stored["name"],
                            "image": service_stored["image"] + ":" + service_stored["tags"],
                            "ports": [{"containerPort": int(port)} for port in service_stored["ports"]],
                            **({"env": [{"name": k, "value": v} for k, v in service_stored["environments"].items()]}
                               if "environments" in service_stored and service_stored["environments"] else {}),
                            **({"resources": service_stored["resources"]}
                               if "resources" in service_stored and service_stored["resources"] else {}),
                            **({"volumeMounts": [{"name": f"vol{i.replace("/", "-")}", "mountPath": i} for i in service_stored["volumes"]]}
                               if "volumes" in service_stored and service_stored["volumes"] else {})
                        }],
                        **({"volumes": [{"name": f"vol{i.replace("/", "-")}", "persistentVolumeClaim": {"claimName": f"pvc{i.replace("/", "-")}"}} for i in service_stored["volumes"]]}
                           if "volumes" in service_stored and service_stored["volumes"] else {})
                    },
                },
            },
        })

        ## PVC
        for path, size in service_stored["volumes"].items():
            manifests.append({
                "apiVersion": "v1",
                "kind": "PersistentVolumeClaim",
                "metadata":{
                    "name": f"pvc{path.replace("/", "-")}"
                },
                "spec":{
                    "accessModes": [
                        "ReadWriteOnce"
                    ],
                    "resources": {
                        "requests": {
                            "storage": size
                        }
                    }
                }
            })

        ## Services
        manifests.append({
            "apiVersion": "v1",
            "kind": "Service",
            "metadata":{
                "name": f"svc-{service_stored["name"]}",
                "labels": {
                    "app": service_stored["name"],
                    **({"labels": service_stored["labels"]} if "labels" in service_stored and service_stored[
                        "labels"] else {})
                }
            },
            "spec": {
                "type": service_stored["service_type"],
                "selector": {
                    "app": service_stored["name"],
                    **({"labels": service_stored["labels"]} if "labels" in service_stored and service_stored[
                        "labels"] else {})
                },
                "ports": [
                    {"protocol": "TCP", "port": int(port), "targetPort": int(port)} for port in service_stored["ports"]
                ]
            }
        })


    return yaml.dump_all(manifests, default_flow_style=False)
