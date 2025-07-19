"""Entropy-based validation utilities."""
import math
from collections import Counter

def text_entropy(s):
    """Calculate Shannon entropy for the given string."""
    if not s:
        return 0.0
    freq = Counter(s)
    total = len(s)
    return -sum((count/total) * math.log2(count/total) for count in freq.values())

def compute_stats(ocr_texts):
    """
    Given a list of OCR output strings, return stats for each:
    - length
    - entropy
    """
    stats = []
    for text in ocr_texts:
        ent = text_entropy(text)
        stats.append({'length': len(text), 'entropy': ent})
    return stats

def detect_outlier_indices(stats, threshold=2.0):
    """
    Flag indices that are >threshold standard deviations away from mean
    for either length or entropy.
    """
    import numpy as np
    lens = np.array([s['length'] for s in stats])
    ents = np.array([s['entropy'] for s in stats])
    mean_len, std_len = lens.mean(), lens.std()
    mean_ent, std_ent = ents.mean(), ents.std()

    outlier_indices = []
    for i, s in enumerate(stats):
        if abs(s['length'] - mean_len) > threshold * std_len or \
           abs(s['entropy'] - mean_ent) > threshold * std_ent:
            outlier_indices.append(i)
    return outlier_indices
