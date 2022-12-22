import os
import cv2

ROOT_PATH = "C:/dev/draft"
VIDEO_PATH = ROOT_PATH + "/video"
IMAGE_PATH = ROOT_PATH + "/image"

TIME_MEASUERMENT_UNIT = 60

if not os.path.exists(VIDEO_PATH):
    os.mkdir(VIDEO_PATH)

def save(name):
    if not os.path.exists(IMAGE_PATH + f"/{name}"):
        os.mkdir(IMAGE_PATH + f"/{name}")
    
    video = cv2.VideoCapture(VIDEO_PATH + f"/{name}.mp4")

    while video.isOpened():
        ret,frame = video.read()

        if ret:
        # 현재 프레임 위치 (msec) 
            frame_sec = video.get(cv2.CAP_PROP_POS_MSEC)/1000
            if frame_sec.is_integer():
                if (frame_sec % TIME_MEASUERMENT_UNIT < 5):
                    filename = IMAGE_PATH + f"/{name}" +"/" + str(round(frame_sec)) + ".jpg"
                    cv2.imwrite(filename, frame) 
        else:
            break
