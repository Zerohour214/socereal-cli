from src.modules.validations.symbol_validation import validate_text

# A mock OCRService for testing
class MockOCRService:
    def __init__(self, outputs):
        self.outputs = outputs
        self.index = 0

    def image_to_text(self, img_path):
        out = self.outputs[self.index]
        self.index += 1
        return out
def run_ocr_pipeline_val(image_paths, ocr_service):
    """Minimal version for testing: runs OCR and validates, returns output for assertions."""
    results = []
    for img_path in image_paths:
        text = ocr_service.image_to_text(img_path)
        val_msg = validate_text(text)
        results.append((img_path, text, val_msg or "OK"))
    return results

def test_run_ocr_pipeline_val_validation():
    # Arrange
    image_files = ["img1.jpg","img2.jpg","img3.jpg"]
    mock_outputs = [
        # 0: Normal, ASCII, single line
        "This is clean text.",
        # 1: Multi-line with tabs and spaces (should be OK)
        "SerialNumber:\t1234-5678\nBatch: 42",
        # 2: Only whitespace (should be flagged as empty)
        "    \t   \n",
        # 3: Emoji/symbols (should be flagged abnormal)
        "S/N: 1234-5678 ☠️",
        # 4: Non-ASCII letters (should be flagged abnormal)
        "Serial: 1234-Ω-5678",
        # 5: CJK (Chinese/Japanese/Korean, abnormal)
        "序列号: 1234-5678",
        # 6: Broken Unicode (zero-width space, abnormal)
        "SN1234\u200B5678",
        # 7: Mixed allowed and weird (math symbol, abnormal)
        "ABC1234÷5678",
        # 8: All allowed symbols (should be OK)
        "SN#1234_$-ABCD/EFG+9876~`",
        # 9: Control character (vertical tab, abnormal)
        "S/N: 1234-5678\v",
        # 10: Edge-case: long, valid, with lots of symbols and whitespace
        "ABCD-1234_56.78/A:1+B  \n\t##--==__//..++"
    ]

    expected_results = [
        "OK",  # 0
        "OK",  # 1
        "Empty or whitespace-only OCR result",  # 2
        "Abnormal characters detected",  # 3
        "Abnormal characters detected",  # 4
        "Abnormal characters detected",  # 5
        "Abnormal characters detected",  # 6
        "Abnormal characters detected",  # 7
        "OK",  # 8
        "Abnormal characters detected",  # 9
        "OK",  # 10
    ]

    image_files = [f"img{i}.jpg" for i in range(len(mock_outputs))]
    ocr_service = MockOCRService(mock_outputs)
    results = run_ocr_pipeline_val(image_files, ocr_service)

    for i, (img, text, verdict) in enumerate(results):
        print(f"{i}: {repr(text)} => {verdict}")
        if expected_results[i] == "OK":
            assert verdict == "OK"
        elif expected_results[i].startswith("Abnormal"):
            assert verdict.startswith("Abnormal characters detected")
        else:
            assert verdict == expected_results[i]
