def get_average_confidence(result):
    """
    Given a RapidOCROutput result, return the average confidence score (float).
    """
    if not hasattr(result, "scores") or not result.scores:
        return 0.0
    return sum(result.scores) / len(result.scores)

def validate_confidence(result, threshold=0.90):
    """
    Return "OK" if average confidence is above threshold,
    else a warning string.
    """
    avg_conf = sum(conf for _, _, conf in result) / len(result)
    if avg_conf < threshold:
        return f"Low confidence: {avg_conf:.2f}"
    return "OK"

def extract_text_and_conf(result):
    if hasattr(result, "txts") and hasattr(result, "scores"):
        text = " ".join(result.txts) if result.txts else ""
        return text, result
    # List of (bbox, text, conf) -- element can be tuple OR list
    elif isinstance(result, list) and result and isinstance(result[0], (tuple, list)) and len(result[0]) == 3:
        text = " ".join([t for _, t, _ in result])
        return text, result
    # Plain text
    elif isinstance(result, str):
        return result, None
    return "", None
