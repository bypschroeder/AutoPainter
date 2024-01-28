from logging import Logger

from object_detection.capture_webcam import capture_webcam
from object_detection.detect_numbers import recognize_numbers, detect_dots_numbers
import cv2
import customtkinter
import dobot.dobot_controller as dobot_controller


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
    # print(data)
    img = cv2.imread(CAPTURED_IMG_PATH)

    for number, coordinates in data:
        x, y = coordinates
        x = int((x / 100) * 1080) + 420
        y = int((y / 100) * 1080)

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), 3)

    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    numbers = [item[0] for item in data if item[0] is not None]

    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")

    app = customtkinter.CTk()
    app.geometry("800x600")
    app.title("Ausgabe")

    l1 = customtkinter.CTkLabel(master=app, text=f"Erkannte Zahlen: {numbers}", font=("Arial", 24))
    l1.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)
    l2 = customtkinter.CTkLabel(master=app, text="Homing ausführen!", font=("Arial", 32), text_color="red")
    l2.place(relx=0.5, rely=0.55, anchor=customtkinter.CENTER)

    def button_function():
        app.destroy()

    def cancel_application():
        app.destroy()
        raise SystemExit

    button = customtkinter.CTkButton(
        master=app,
        text="OK",
        command=button_function,
        font=("Arial", 20),
        width=200,
        height=50,
        corner_radius=8
    )
    button.place(relx=0.35, rely=0.9, anchor=customtkinter.CENTER)
    button2 = customtkinter.CTkButton(
        master=app,
        text="Abbrechen",
        command=cancel_application,
        font=("Arial", 20),
        fg_color="#6A8194",
        hover_color="#434F58",
        width=200,
        height=50,
        corner_radius=8
    )
    button2.place(relx=0.65, rely=0.9, anchor=customtkinter.CENTER)

    app.mainloop()

    logger = Logger(name="dobot")
    dobot = dobot_controller.DobotController(logger=logger, port=1)
    # coords_to_draw = [(0, 0), (100, 0), (100, 100), (0, 100), (0, 0)]
    # dobot.draw_dot_to_dot(coords_to_draw)
