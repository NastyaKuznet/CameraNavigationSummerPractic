import cv2
from ultralytics import YOLO
from keras_facenet import FaceNet

embedder = FaceNet()
xmtcnn = embedder.mtcnn()
model = YOLO("yolov8n.pt")
video = cv2.VideoCapture("rtsp://192.168.1.2:9999/h264.sdp")  # "rtsp://192.168.1.2:9999/h264.sdp"

frame_skip = 60  # Количество кадров для пропуска
frame_count = 0

while True:
    ret, frame = video.read()

    if not ret:
        break

    frame_count += 1
    if frame_count % (frame_skip + 1) != 0:
        continue

    # Faces
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = xmtcnn.detect_faces(frame)

    for i in range(len(faces)):
        x, y, w, h = faces[i]['box']
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

    img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Track objects
    results = model.track(img_color, persist=True)

    # for box in results[0].boxes.xywh:
    #     x, y, w, h = [int(i) for i in box]
    #     cv2.rectangle(img_color, (x//2, y//2), (x + w//2, y + h//2), (255, 0, 0))

    res_plotted = results[0].plot()
    cv2.imshow(f"Tracking_Stream", res_plotted)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release video sources
video.release()
cv2.destroyAllWindows()
