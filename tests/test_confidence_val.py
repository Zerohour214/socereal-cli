from src.modules.validations.confidence_validation import get_average_confidence, validate_confidence

def test_get_average_confidence():
    # 1. Normal case
    result = [([0,0,1,1], "ABC", 0.9), ([2,2,3,3], "123", 0.8)]
    assert abs(get_average_confidence(result) - 0.85) < 1e-6

    # 2. All high
    result = [([0], "A", 1.0), ([1], "B", 1.0)]
    assert get_average_confidence(result) == 1.0

    # 3. Empty result
    assert get_average_confidence([]) == 0.0

def test_validate_confidence():
    # 1. Passes threshold
    result = [([0], "A", 0.9), ([1], "B", 0.92)]
    assert validate_confidence(result, threshold=0.85) == "OK"

    # 2. Fails threshold
    result = [([0], "A", 0.7), ([1], "B", 0.8)]
    assert validate_confidence(result, threshold=0.85).startswith("Low confidence")

    # 3. Empty result
    assert validate_confidence([], threshold=0.85).startswith("Low confidence")
