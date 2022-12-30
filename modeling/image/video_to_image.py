import os
import cv2

ROOT_PATH = "./image/data"
VIDEO_PATH = ROOT_PATH + "/video"
IMAGE_PATH = ROOT_PATH + "/image"

TIME_MEASUERMENT_UNIT = 1

def save():
    
    files = os.listdir(VIDEO_PATH)
    
    for file in files:
        # NEW_PATH = IMAGE_PATH + "/" + os.path.splitext(file)
        # if not os.path.exists(NEW_PATH):
        #     os.mkdir(NEW_PATH)
        
        path = os.path.join(VIDEO_PATH, file)
        video = cv2.VideoCapture(path)
        i = 0
        while video.isOpened():
            ret,frame = video.read()

            if ret:
                if i > 5:
                    break
            # 현재 프레임 위치 (msec) 
                frame_sec = video.get(cv2.CAP_PROP_POS_MSEC)/1000
                if frame_sec.is_integer():
                    if (frame_sec % TIME_MEASUERMENT_UNIT == 0 ):
                        filename = IMAGE_PATH +"/" + str(round(frame_sec)) + ".jpg"
                        cv2.imwrite(filename, frame)
                        i+=1
            else:
                break
