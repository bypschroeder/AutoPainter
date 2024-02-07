import cv2
import numpy as np
import supervision as sv
from object_detection.detect_numbers import delete_folder_contents, load_model


def segment_instances():
    """
    Segments the instances of the captured image and returns the polygons of the detected objects.
    :return: polygons: List of polygons of the detected objects
    """

    from app import OBJECT_SEGMENTATION_MODEL_PATH, CAPTURED_IMG_PATH, SAVE_DIR, RESULT_WINDOW_WIDTH, RESULT_WINDOW_HEIGHT, SHOW_POLYGONS

    delete_folder_contents(SAVE_DIR)

    model = load_model(OBJECT_SEGMENTATION_MODEL_PATH)
    img = cv2.imread(CAPTURED_IMG_PATH)

    results = model(img, conf=0.5, save=True, save_crop=True, project=SAVE_DIR)[0]
    detections = sv.Detections.from_ultralytics(results)

    polygons = [sv.mask_to_polygons(m) for m in detections.mask]

    img_with_polygons = img.copy()
    for poly in polygons:
        for p in poly:
            points = p.reshape((-1, 1, 2))
            cv2.polylines(img_with_polygons, [points], True, (0, 255, 0), 2)

    if SHOW_POLYGONS:
        cv2.namedWindow('Object Segmentations', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Object Segmentations', RESULT_WINDOW_WIDTH, RESULT_WINDOW_HEIGHT)
        cv2.imshow('Object Segmentations', img_with_polygons)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return polygons


def convert_coordinates_poly(poly_coords):
    """
    Converts the coordinates of the detected polygons to a format that can be used by the Dobot.
    :param poly_coords: List of polygons of the detected objects
    :return: converted_data: List of converted coordinates for the detected polygons
    """

    converted_data = []

    for polygons in poly_coords:
        polygon_data = []
        previous_point = None

        for poly in polygons:
            for point in poly:
                if isinstance(point, (np.int64, np.float64)):
                    continue

                x = point[0]
                y = point[1]

                if x > 882:
                    x -= 882

                new_x = round((x / 2268) * 100, 2)
                new_y = round((y / 2268) * 100, 2)

                if previous_point is not None:
                    diff_x = abs(new_x - previous_point[0])
                    diff_y = abs(new_y - previous_point[1])

                    if diff_x > 0.1 or diff_y > 0.1:
                        polygon_data.append((new_x, new_y))

                previous_point = (new_x, new_y)

        converted_data.append(polygon_data)

    return converted_data
