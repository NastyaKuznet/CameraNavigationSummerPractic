import cv2
from ultralytics import YOLO
from keras_facenet import FaceNet
import numpy as np

embedder = FaceNet()
xmtcnn = embedder.mtcnn()
model = YOLO("yolov8n.pt")
video = cv2.VideoCapture(0)  # "rtsp://192.168.1.2:9999/h264.sdp"

# frame_skip = 60  # Количество кадров для пропуска
# frame_count = 0


def get_embedding(img):
    try:
        face_img = img.astype('float32')
        face_img = np.expand_dims(face_img, axis=0)
        yhat = embedder.embeddings(face_img)  # 512
        return yhat[0]
    except Exception:
        pass

def recognize(embedding_vec):
    pass

last_ids = {}

while True:
    ret, frame = video.read()

    if not ret:
        break

    # frame_count += 1
    # if frame_count % (frame_skip + 1) != 0:
    #     continue

    # Faces
    img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Track objects
    results = model.track(img_color, persist=True, show=False)
    # 0 is a person
    # print(results[0].boxes.cls.cpu().numpy())  # [          0           0]
    # print(results[0].boxes.id)  # tensor([2., 4.])

    if results[0].boxes:
        classes = results[0].boxes.cls.cpu().numpy()
        boxes = results[0].boxes.xywh
        for clas, box in zip(classes, boxes):
            if int(clas) != 0:
                continue
            x, y, w, h = box
            cv2.rectangle(img_color, (int(x-w//2), int(y-h//2)), (int(x+w//2), int(y+h//2)), (255, 0, 0))
            faces = xmtcnn.detect_faces(img_color[int(y-h//2):int(y+h//2), int(x-w//2):int(x+w//2)])
            for k in range(len(faces)):
                x1, y1, w1, h1 = faces[k]['box']
                cv2.rectangle(img_color, (x1+int(x-w//2), y1+int(y-h//2)), (x1+int(x-w//2) + w1, y1+int(y-h//2) + h1),
                              (0, 0, 255))
                embedding = get_embedding(img_color[y1+int(y-h//2):y1+int(y-h//2) + h1,
                                          x1+int(x-w//2):x1+int(x-w//2) + w1])
                #  Далее распознаем

    # faces = xmtcnn.detect_faces(img_color)
    # embeddings = []
    # for k in range(len(faces)):
    #     x, y, w, h = faces[k]['box']
    #     cv2.rectangle(img_color, (x, y), (x + w, y + h), (0, 0, 255))
    #     try:
    #         face_img = img_color[x:x+w, y:y+h].astype('float32')
    #         face_img = np.expand_dims(face_img, axis=0)
    #         yhat = embedder.embeddings(face_img)  # 512
    #         embeddings.append(yhat[0])
    #     except Exception:
    #         pass

    img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

    # if results[0].boxes.id:
    #     recognize = False
    #     for i in results[0].boxes.id:
    #         if i not in last_ids:
    #             last_ids[i] = 0
    #             recognize = True
    #     if recognize:
    #         faces = xmtcnn.detect_faces(frame)
    #         print(faces[0]['confidence'])
    #         for k in range(len(faces)):
    #             x, y, w, h = faces[k]['box']
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
    #
    #         img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     elif 0 in last_ids.values():
    #         faces = xmtcnn.detect_faces(frame)
    #
    #         for k in range(len(faces)):
    #             x, y, w, h = faces[k]['box']
    #             cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
    #
    #         img_color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #     for j in last_ids:
    #         if j not in results[0].boxes.id:
    #             last_ids.pop(j)

    # for box in results[0].boxes.xywh:
    #     x, y, w, h = [int(i) for i in box]
    #     cv2.rectangle(img_color, (x//2, y//2), (x + w//2, y + h//2), (255, 0, 0))

    # res_plotted = results[0].plot()
    cv2.imshow(f"Tracking_Stream", img_color)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release video sources
video.release()
cv2.destroyAllWindows()
