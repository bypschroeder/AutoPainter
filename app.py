from object_detection.capture_webcam import capture_webcam
from object_detection.detect_numbers import recognize_numbers, detect_dots_numbers
import cv2


MODEL_PATH = "resources/yolo_model/best.pt"
CAPTURED_IMG_PATH = "resources/captured_img/4.jpg"
SAVE_DIR = "resources/runs/detect/"
PYTESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract.exe"


def run():
    """
    Runs the application.
    """

    # capture_webcam(CAPTURED_IMG_PATH)

    data = recognize_numbers(detect_dots_numbers())
    print(data)
    img = cv2.imread(CAPTURED_IMG_PATH)

    for number, coordinates in data:
        x, y = coordinates
        x = int((x / 100) * 1080) + 420
        y = int((y / 100) * 1080)

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), 3)

    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
