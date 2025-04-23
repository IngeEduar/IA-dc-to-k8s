from src.nlp.spacy.matcher import train_matcher


def get_data_from_text(text: str) -> dict:
    nlp, matcher = train_matcher()
    doc = nlp(text.lower())
    matches = matcher(doc)

    result = init_result()
    temp_resources = init_temp_resources()

    process_entities(doc, result, temp_resources)
    process_matches(matches, doc, result)

    result["resources"] = temp_resources

    if not result["has_volume"]:
        result["volume_detail"] = {}
    if not result["create_ingress"]:
        result["ingress"] = {}

    return result


def init_result() -> dict:
    return {
        "return_yaml": False,
        "port": None,
        "create_service": False,
        "service_type": "ClusterIP",
        "create_ingress": False,
        "ingress": {
            "host": "www.example.com",
            "path": "/",
            "tls_secret": "secret-tls"
        },
        "configmap": [],
        "has_volume": False,
        "name": None,
        "labels": {},
        "image": None,
        "namespace": "default",
        "command": [],
        "args": [],
        "volume_detail": {
            "name": "default-volume",
            "type": "emptyDir",
            "path": "/tmp"
        },
        "kind": "Deployment",
        "resources": {},
        "containers": 1
    }


def init_temp_resources() -> dict:
    return {
        "limits": {"memory": None, "cpu": None},
        "requests": {"memory": None, "cpu": None}
    }


def process_entities(doc, result: dict, temp_resources: dict):
    for ent in doc.ents:
        label = ent.label_
        tokens = [token.text for token in ent]

        match label:
            case "YAML":
                result["return_yaml"] = True
            case "INGRESS":
                result["create_ingress"] = True
            case "VOLUME":
                result["has_volume"] = True
            case "KIND":
                result["kind"] = tokens[0].capitalize()
            case "IMAGE":
                result["image"] = tokens[1] if len(tokens) > 1 else tokens[0]
            case "RESOURCE_MEMORY_LIMIT":
                temp_resources["limits"]["memory"] = f"{tokens[0]}{tokens[1]}"
            case "RESOURCE_CPU_LIMIT":
                temp_resources["limits"]["cpu"] = tokens[0]
            case "RESOURCE_MEMORY_REQUEST":
                temp_resources["requests"]["memory"] = f"{tokens[0]}{tokens[1]}"
            case "RESOURCE_CPU_REQUEST":
                temp_resources["requests"]["cpu"] = tokens[0]


def process_matches(matches, doc, result: dict):
    for match_id, start, end in matches:
        span = doc[start:end]
        label = doc.vocab.strings[match_id]
        tokens = [token.text for token in span]

        match label:
            case "PORT":
                try:
                    result["port"] = int(tokens[-1])
                except ValueError:
                    pass
            case "SERVICE_NAME":
                result["name"] = tokens[-1]
            case "LABEL":
                if len(tokens) >= 4:
                    result["labels"][tokens[1]] = tokens[3]
            case "CONFIGMAP_EXTRA":
                if len(tokens) >= 4:
                    file_name = tokens[1]
                    content = tokens[3]
                    result["configmap"].append({
                        "file": file_name,
                        "mountPath": f"/tmp/{file_name}",
                        "content": content
                    })
            case "NAMESPACE":
                if len(tokens) >= 2:
                    result["namespace"] = tokens[1]
            case "COMMAND":
                if len(tokens) >= 2:
                    result["command"].append(tokens[1])
            case "ARGS":
                if len(tokens) >= 2:
                    result["args"].append(tokens[1])
            case "RESOURCES":
                if len(tokens) >= 4:
                    result["resources"][tokens[1]] = tokens[3]
