import cv2
from ultralytics import YOLO
import time

yolo = YOLO('yolov8s.pt')
input_video_path = 'static/test video/tester.mp4'
cap = cv2.VideoCapture(input_video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = yolo(frame)
    boxes = results[0].boxes.xyxy
    classes = results[0].boxes.cls

    for box, cls in zip(boxes, classes):
        x1, y1, x2, y2 = map(int, box)
        label = f"Class {int(cls)}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow("YOLOv8 Object Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('c'):
        break

cap.release()
cv2.destroyAllWindows()