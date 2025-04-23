import re


def spam_detector(word):
    return False
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{5,}", word, re.IGNORECASE):
        return True

    if not re.search(r"[aeiouáéíóúü]", word, re.IGNORECASE):
        return True

    if re.search(r"(.)\1{4,}", word):
        return True

    return False


def nonsense_detector(sentence):
    words_list = re.findall(r"\b\w+\b", sentence)

    nonsense_count = sum(1 for word in words_list if spam_detector(word))
    nonsense_ratio = nonsense_count / max(1, len(words_list))

    return nonsense_ratio > 0.3  # Se ajusta el umbral para mayor sensibilidad

