import cv2
import numpy as np
from pyzbar import pyzbar

# Constants
QR_LINE_COLOR = (0, 255, 0)
QR_TEXT_COLOR = (0, 255, 0)
QR_FONT = cv2.FONT_HERSHEY_SIMPLEX
QR_FONT_SCALE = 0.5
QR_FONT_THICKNESS = 2

def process_polygon(points):
    if len(points) > 4:
        hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
        hull = list(map(tuple, np.squeeze(hull)))
    else:
        hull = points

    return hull

def draw_qr_code(frame, obj):
    points = obj.polygon
    hull = process_polygon(points)

    for j in range(len(hull)):
        cv2.line(frame, hull[j], hull[(j + 1) % len(hull)], QR_LINE_COLOR, 3)

    x, y, w, h = obj.rect
    cv2.putText(frame, obj.data.decode("utf-8"), (x, y - 10), QR_FONT, QR_FONT_SCALE, QR_TEXT_COLOR, QR_FONT_THICKNESS)

def decode_qr_codes(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        draw_qr_code(frame, obj)

    return frame

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Webcam not working")
            break

        frame = decode_qr_codes(frame)

        cv2.imshow("QR Code Scanner", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
