import argparse
import cv2


def parse_arguments() -> argparse.Namespace:
    """
    Parse arguments to set webcam resolution
    :return: parsed arguments
    """
    from app import WEBCAM_RESOLUTION_WIDTH, WEBCAM_RESOLUTION_HEIGHT
    parser = argparse.ArgumentParser(description='YOLOv8')
    parser.add_argument(
        '--webcam-resolution',
        default=[WEBCAM_RESOLUTION_WIDTH, WEBCAM_RESOLUTION_HEIGHT],
        nargs=2,
        type=int,
    )
    args = parser.parse_args()
    return args


def capture_webcam(output_file):
    """
    Capture image from webcam
    :param output_file: path to save image
    """

    args = parse_arguments()
    frame_width, frame_height = args.webcam_resolution

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(output_file, frame)
        print(f"Image saved as {output_file}")
    else:
        print("Failed to capture image")

    cap.release()
    cv2.destroyAllWindows()
