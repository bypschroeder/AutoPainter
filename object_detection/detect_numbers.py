import os
import shutil
import math
import cv2
from ultralytics import YOLO
import supervision as sv
import pytesseract


def delete_folder_contents(folder_path):
    from app import SAVE_DIR

    try:
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
        else:
            save_dir = SAVE_DIR
            os.makedirs(save_dir, exist_ok=True)
            raise FileNotFoundError(f"Error: {folder_path} does not exist, creating it now")
    except Exception as e:
        print(f"Failed to delete contents of {folder_path}. Reason: {e}")


def load_model(model_path):
    try:
        return YOLO(model_path)
    except Exception as e:
        print(f"Failed to load model from {model_path}. Reason: {e}")
        return None


def sort_files_by_number(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            files.append(filename)
    files.sort(key=lambda x: int(x.split('image')[1].split('.jpg')[0]))
    return files


def calculate_distance(coord1, coord2):
    x1, y1, _, _ = coord1[1]
    x2, y2, _, _ = coord2[1]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def process_image(model, img_path):
    from app import SAVE_DIR

    img = cv2.imread(img_path)

    results = model(img, conf=0.3, project=SAVE_DIR, save=True, save_crop=True)[0]
    detections = sv.Detections.from_ultralytics(results)

    numbers = sort_files_by_number(f"{SAVE_DIR}/predict/crops/Number")
    dots = sort_files_by_number(f"{SAVE_DIR}/predict/crops/Dot")

    classes = []
    for _, _, _, class_id, _ in detections:
        classes.append(class_id)

    coords = []
    for bbox in detections.xyxy:
        x_min, y_min, x_max, y_max = bbox
        coords.append((x_min, y_min, x_max, y_max))

    number_coords = []
    dot_coords = []

    number_index = 0
    dot_index = 0

    for i in range(len(classes)):
        if classes[i] == 1:
            number_coords.append(('number', coords[i], numbers[number_index]))
            number_index += 1
        elif classes[i] == 0:
            dot_coords.append(('dot', coords[i], dots[dot_index]))
            dot_index += 1

    return number_coords, dot_coords, detections, img


def detect_dots_numbers():
    from app import MODEL_PATH, CAPTURED_IMG_PATH, SAVE_DIR

    folder_path = SAVE_DIR

    delete_folder_contents(folder_path)

    model = load_model(MODEL_PATH)

    number_coords, dot_coords, detections, img = process_image(model, CAPTURED_IMG_PATH)

    grouped_coords = []

    for number_coord in number_coords:
        for dot_coord in dot_coords:
            if calculate_distance(number_coord, dot_coord) < 100:
                grouped_coords.append((number_coord, dot_coord))

    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    labels = [
        f"{model.names[class_id]} {confidence:.2f}"
        for _, _, confidence, class_id, _
        in detections
    ]

    img = box_annotator.annotate(
        scene=img,
        detections=detections,
        labels=labels,
    )

    # cv2.imshow('yolov8', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return grouped_coords


def convert_coordinates(grouped_coords):
    converted_data = []

    for number_coords, dot_coords, number in grouped_coords:
        _, (dot_x_min, dot_y_min, dot_x_max, dot_y_max), _ = dot_coords

        center_x = (dot_x_min + dot_x_max) / 2
        center_y = (dot_y_min + dot_y_max) / 2

        if center_x > 420:
            center_x -= 420
        new_center_x = round((center_x / 1080) * 100, 2)
        new_center_y = round((center_y / 1080) * 100, 2)

        converted_data.append((number, (new_center_x, new_center_y)))

    return converted_data


def recognize_numbers(img_coordinates):
    from app import PYTESSERACT_PATH, SAVE_DIR

    pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH
    detection_info = []
    converted_coordinates = []

    for number_info, dot_info in img_coordinates:
        number_img = cv2.imread(f"{SAVE_DIR}predict/crops/Number/{number_info[2]}")
        number_img = cv2.resize(number_img, (0, 0), fx=2, fy=2)
        number_img = cv2.cvtColor(number_img, cv2.COLOR_BGR2GRAY)
        number_img = cv2.threshold(number_img, 125, 255, cv2.THRESH_BINARY)[1]
        config_number = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
        detected_number = pytesseract.image_to_string(number_img, config=config_number)
        cleaned_number = ''.join(filter(str.isdigit, detected_number))

        try:
            number = int(cleaned_number)
        except ValueError:
            number = None

        detection_info.append((number_info, dot_info, number))
        # print(number)

        converted_coordinates = convert_coordinates(detection_info)
        # cv2.imshow("Result", number_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    filtered_data = [coord for coord in converted_coordinates if coord[0] is not None]

    if not filtered_data:
        print("No numbers detected")
        return None
    else:
        sorted_data = sorted(filtered_data, key=lambda item: item[0])
        return sorted_data
