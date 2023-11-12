import cv2
from pyzbar import pyzbar

def decode_qr_codes(frame):
    decoded_objects = pyzbar.decode(frame)
    for obj in decoded_objects:
        points = obj.polygon

        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        for j in range(len(hull)):
            cv2.line(frame, hull[j], hull[(j + 1) % len(hull)], (0, 255, 0), 3)

        x, y, w, h = obj.rect
        cv2.putText(frame, obj.data.decode("utf-8"), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
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
