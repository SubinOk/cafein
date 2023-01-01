from yolov3 import detect
import argparse
import os
import video_to_image
import pandas as pd

# ====== Arguments Initialization ====== #
parser = argparse.ArgumentParser()
args = parser.parse_args("")

# args.weights = './modeling/image/yolov3/pretrained/yolov3.pt'
# args.source = './modeling/image/data/image'
# args.project = './modeling/image/result'
args.source = './image/data/image'
args.project = './image/result'

args.name = 'exp'
args.save_txt = True  
args.nosave = True 
args.classes = 0 # person
# ================================= #


if __name__ == "__main__":
    
    video_to_image.save()
    detect.main(args)

    #root_dir = "./modeling/image/result/" + args.name + "/labels"
    root_dir = "./image/result/" + args.name + "/labels"
    files = os.listdir(root_dir)

    cnt = 0
    for file in files:
        path = os.path.join(root_dir, file)
        label = open(path, 'r')
        cnt += len(label.readlines())

    print("현재 사람 수: ", round(cnt/len(files)))
    people_cnt = round(cnt/len(files))

    result = pd.DataFrame({'people':people_cnt}, index=[0])
    result.to_csv("./../frontend/cafein/cafein/files/result/temp.csv", index=False)
