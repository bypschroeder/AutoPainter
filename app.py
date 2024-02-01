from logging import Logger

from object_detection.capture_webcam import capture_webcam
from object_detection.detect_numbers import recognize_numbers, detect_dots_numbers
import cv2
import customtkinter
import dobot.dobot_controller as dobot_controller

# Path of the trained yolo model
MODEL_PATH = "resources/yolo_model/best.pt"
# Path where the captured image will be saved
CAPTURED_IMG_PATH = "resources/captured_img/4.jpg"
# Path where the detected image will be saved
SAVE_DIR = "resources/runs/detect"
# Path to the tesseract executable
PYTESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Webcam Settings
CAPTURE_WEBCAM = False
WEBCAM_RESOLUTION_WIDTH = 1920
WEBCAM_RESOLUTION_HEIGHT = 1080

# Options to show results
SHOW_DETECTIONS = False  # Show the detections of the yolo model
SHOW_CROPPED_NUMBER = False  # Show the cropped number with their recognized value
SHOW_DETECTED_DOTS = True  # Show the order of the detected dots

# Detection Settings
CONFIDENCE_THRESHOLD = 0.1  # Threshold for the confidence of the yolo model detection
RESIZE_FACTOR = 2  # Factor to resize the cropped, detected number
THRESHOLD_VALUE = 140  # Threshold value for the grayscale image of the cropped, detected number
THRESHOLD_MAX_VALUE = 255  # Max value for the threshold_value

# Result Window Resolution
RESULT_WINDOW_WIDTH = 1920
RESULT_WINDOW_HEIGHT = 1080

# COM-Port of the Dobot
DOBOT_PORT = 2


def run():
    """
    Runs the application.
    """

    # Capture image from webcam
    if CAPTURE_WEBCAM:
        capture_webcam(CAPTURED_IMG_PATH)

    # Detect Numbers and Dots
    data = recognize_numbers(detect_dots_numbers())

    # Show detections
    if SHOW_DETECTED_DOTS:
        img = cv2.imread(CAPTURED_IMG_PATH)

        for number, coordinates in data:
            x, y = coordinates
            x = int((x / 100) * 1080) + 420
            y = int((y / 100) * 1080)

            cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), 3)

            label = f"{number}"
            cv2.putText(img, label, (int(x) - 15, int(y) - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Result", RESULT_WINDOW_WIDTH, RESULT_WINDOW_HEIGHT)
        cv2.imshow("Result", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Only recognized numbers
    numbers = [item[0] for item in data if item[0] is not None]

    # Show GUI
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("800x600")
    app.title("Output")

    # Labels of the GUI
    l1 = customtkinter.CTkLabel(master=app, text=f"Recognized Numbers: {numbers}", font=("Arial", 24))
    l1.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)
    l2 = customtkinter.CTkLabel(master=app, text="Execute homing of Dobot!", font=("Arial", 32), text_color="red")
    l2.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)

    def button_function():
        app.destroy()

    def cancel_application():
        app.destroy()
        raise SystemExit

    # Buttons of the GUI
    button = customtkinter.CTkButton(
        master=app,
        text="Continue",
        command=button_function,
        font=("Arial", 20),
        width=200,
        height=50,
        corner_radius=8
    )
    button.place(relx=0.35, rely=0.9, anchor=customtkinter.CENTER)
    button2 = customtkinter.CTkButton(
        master=app,
        text="Cancel",
        command=cancel_application,
        font=("Arial", 20),
        fg_color="#6A8194",
        hover_color="#434F58",
        width=200,
        height=50,
        corner_radius=8
    )
    button2.place(relx=0.65, rely=0.9, anchor=customtkinter.CENTER)

    # Run GUI
    app.mainloop()

    # Shape data to coordinates only
    coordinates_only = [coordinates for _, coordinates in data]
    print(coordinates_only)

    # Connect to Dobot
    logger = Logger(name="dobot")
    dobot = dobot_controller.DobotController(logger=logger, port=DOBOT_PORT)

    # Draw dot to dot
    if dobot.is_connected:
        dobot.draw_dot_to_dot(coordinates_only)
