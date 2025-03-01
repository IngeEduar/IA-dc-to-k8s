import json, os

main_path = os.path.abspath(os.path.join("src/nlp/model/data"))

def get_data():
    response = []
    files = [
        "mongodb.json",
        "redis.json",
        "postgresql.json",
        "mysql.json",
        "elasticsearch.json",
        "nginx.json",
        "yaml.json",
        "greet.json"
    ]

    for file in files:
        with open(f"{main_path}/{file}", "r", encoding="utf-8") as jsonfile:
            response.append(json.load(jsonfile))

    return response