import cv2
import os


class VidToImgs:
    @staticmethod
    def extract_frames(video_path, output_folder, counter):
        frame_skip = 2  # Количество кадров для пропуска
        frame_count = 0

        video = cv2.VideoCapture(video_path)

        if not video.isOpened():
            print("Video opening error")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Counter is number which concatenate to name (for copies). Becareful to won't overwrite already exists img
        frame_count = 0
        while True:
            frame_count += 1
            if frame_count % frame_skip != 0:
                continue

            success, frame = video.read()

            # If we can't read, video is over
            if not success:
                break

            # Save image
            frame_path = os.path.join(output_folder, f"{os.path.basename(video_path)}{frame_count}.jpg")
            cv2.imwrite(frame_path, frame)


        video.release()


if __name__ == '__main__':
    vti = VidToImgs()

    video_path = r"D:\загрузки\domofon\p2 12-09-41 12-10-11.flv"
    output_folder = r"D:\Python\CameraNavigation\CameraNavigationSummerPractic\resources\sequences\cam2"

    vti.extract_frames(video_path, output_folder, 0)
