import yaml

from src.data.services.services import get_service_data, generate_new_service_data

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
                            **({"volumeMounts": [{"name": f"vol{i.replace('/', '-')}", "mountPath": i} for i in service_stored["volumes"]]}
                               if "volumes" in service_stored and service_stored["volumes"] else {})
                        }],
                        **({"volumes": [{"name": f"vol{i.replace('/', '-')}", "persistentVolumeClaim": {"claimName": f"pvc{i.replace('/', '-')}"}} for i in service_stored["volumes"]]}
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
                    "name": f"pvc{path.replace('/', '-')}"
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
                "name": f"svc-{service_stored['name']}",
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
