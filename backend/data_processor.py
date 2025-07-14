import re
from typing import Dict


def extract_features(text: str) -> Dict[str, float]:
    """Extract simple numeric features from text."""
    tokens = re.findall(r"\b\w+\b", text)
    num_words = len(tokens)
    avg_word_len = sum(len(tok) for tok in tokens) / num_words if num_words else 0
    num_digits = sum(ch.isdigit() for ch in text)
    num_upper = sum(ch.isupper() for ch in text)
    return {
        "num_words": num_words,
        "avg_word_len": avg_word_len,
        "num_digits": num_digits,
        "num_uppercase": num_upper,
    }
