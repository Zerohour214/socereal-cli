"""Validation helpers for OCR confidence scores."""
def get_average_confidence(result):
    """Return the average confidence score from a RapidOCR result."""
    if hasattr(result, "scores") and result.scores:
        return sum(result.scores) / len(result.scores)
    if isinstance(result, list) and result:
        try:
            # Validate that each element is a sequence with at least two elements
            if all(isinstance(item, (tuple, list)) and len(item) >= 2 for item in result):
                return sum(conf for *_ , conf in result) / len(result)
        except (ValueError, TypeError) as e:
            # Log or handle the error appropriately (e.g., print or log the exception)
            pass
    return 0.0

def validate_confidence(result, threshold=0.90):
    """Return a verdict string based on the average confidence score."""
    avg_conf = get_average_confidence(result)
    if avg_conf < threshold:
        return f"Low confidence: {avg_conf:.2f}"
    return "OK"

def extract_text_and_conf(result):
    """Return extracted text and confidence structure from various result formats."""
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
