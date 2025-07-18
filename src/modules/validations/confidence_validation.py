def get_average_confidence(result):
    """
    Given an OCR result as a list of (bbox, text, confidence) tuples,
    return the average confidence score (float).
    """
    if not result:
        return 0.0
    confidences = [conf for _, _, conf in result]
    return sum(confidences) / len(confidences)

def validate_confidence(result, threshold=0.80):
    """
    Return "OK" if average confidence is above threshold,
    else a warning string.
    """
    avg_conf = get_average_confidence(result)
    if avg_conf < threshold:
        return f"Low confidence: {avg_conf:.2f}"
    return "OK"
