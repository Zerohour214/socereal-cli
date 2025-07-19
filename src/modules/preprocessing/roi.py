"""Pre-processing helpers for image regions."""
import cv2

def auto_crop_serial_region(
    """Crop the central region of an image used for OCR."""
    image_path, region_height_ratio=0.7, region_width_ratio=0.95
):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)
    h, w = img.shape[:2]
    region_h = int(h * region_height_ratio)
    region_w = int(w * region_width_ratio)
    start_y = max(h // 2 - region_h // 2, 0)
    start_x = max(w // 2 - region_w // 2, 0)
    roi = img[start_y:start_y + region_h, start_x:start_x + region_w]
    cv2.imwrite("autocrop_result.jpg", roi)  # For debug
    return roi
