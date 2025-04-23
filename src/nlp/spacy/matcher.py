import spacy
from spacy.matcher import Matcher
from spacy.pipeline import EntityRuler

def train_matcher():
    nlp = spacy.load("es_core_news_sm")
    matcher = Matcher(nlp.vocab)
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    patterns = [
        {"label": "INGRESS", "pattern": [{"LOWER": "ingress"}]},
        {"label": "VOLUMEN", "pattern": [{"LOWER": {"IN": ["volumen", "volume"]}}]},
        {"label": "CONFIGMAP", "pattern": [{"LOWER": "configmap"}]},
        {"label": "IMAGEN", "pattern": [{"LOWER": {"IN": ["imagen", "image"]}}, {"TEXT": {"REGEX": r".+:.+"}}]},
        {"label": "YAML", "pattern": [{"LOWER": {"IN": ["yaml", "archivo"]}}]},
        {"label": "KIND", "pattern": [{"LOWER": {"IN": ["deployment", "statefulset", "cronjob"]}}]},
        {"label": "RESOURCE_MEMORY_LIMIT",
         "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["gb", "mb"]}}, {"LOWER": "para"}, {"LOWER": "memoria"}]},
        {"label": "RESOURCE_CPU_LIMIT",
         "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["nucleos", "cores"]}}, {"LOWER": "de"}, {"LOWER": "cpu"}]},
        {"label": "RESOURCE_MEMORY_REQUEST",
         "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["gb", "mb", "gib", "mib"]}},
                     {"LOWER": {"IN": ["para", "de"]}}, {"LOWER": "memoria"}]},
        {"label": "RESOURCE_CPU_REQUEST",
         "pattern": [{"LIKE_NUM": True}, {"LOWER": {"IN": ["nucleos", "cores"]}}, {"LOWER": "para"}, {"LOWER": "cpu"}]},
    ]

    ruler.add_patterns(patterns)

    matcher.add("PUERTO", [[{"LOWER": "puerto"}, {"IS_DIGIT": True}]])
    matcher.add("YAML", [[{"LOWER": {"IN": ["yaml", "manifiesto"]}}, {"IS_DIGIT": True}]])
    matcher.add("NOMBRE_SERVICIO", [[{"LOWER": {"IN": ["llamado", "nombre"]}}, {"IS_ALPHA": True}]])
    matcher.add("LABEL", [[{"LOWER": "label"}, {"IS_ALPHA": True}, {"LOWER": "igual"}, {"IS_ALPHA": True}]])
    matcher.add("CONFIGMAP_EXTRA",
                [[{"LOWER": "configmap"}, {"IS_ALPHA": True}, {"LOWER": "igual"}, {"IS_ALPHA": True}]])
    matcher.add("NAMESPACE", [[{"LOWER": "namespace"}, {"IS_ALPHA": True}]])
    matcher.add("COMMAND", [[{"LOWER": "command"}, {"IS_ALPHA": True}]])
    matcher.add("ARGS", [[{"LOWER": "args"}, {"IS_ALPHA": True}]])
    matcher.add("RESOURCES", [[{"LOWER": "recursos"}, {"IS_ALPHA": True}, {"LOWER": "igual"}, {"IS_ALPHA": True}]])

    return nlp, matcher