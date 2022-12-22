from yolov3 import detect
import argparse
import os

import video_to_image

if __name__ == "__main__":
    
    frame_image_save = video_to_image.save('cctv')


# ====== Random Seed Initialization ====== #
parser = argparse.ArgumentParser()
args = parser.parse_args("")

# args.weights = './modeling/image/yolov3/pretrained/yolov3.pt'
args.source = './modeling/image/data'
args.project = './modeling/image/result'
args.name = 'exp2'
args.save_txt = True  
args.nosave = True 
args.classes = 0 # person
# ================================= #

detect.main(args)

root_dir = "./modeling/image/result/" + args.name + "/labels"
files = os.listdir(root_dir)

cnt = 0
for file in files:
    path = os.path.join(root_dir, file)
    label = open(path, 'r')
    cnt += len(label.readlines())

print("현재 사람 수: ", round(cnt/len(files)))