## nlp
- 카페명 및 전화번호를 입력하였을 때, 네이버 지도 내 리뷰를 크롤링하여 키워드, 긍부정 분석을 진행하는 모델입니다.
- [모델 파일을 저장](https://drive.google.com/file/d/16I3DW3GScvwqBDl7yVYvBr9gsa0pVVs7/view)하여 frontend/cafein/owner/model폴더 만드시고 압축을 풀어주세요.
- 사용하는 크롬 브라우저 버전에 맞는 크롬 드라이브를 [설치](https://chromedriver.chromium.org/downloads)해주세요.

<br>

## image
- 동영상이 주어졌을 때, 동영상을 단위 시간에 따라 이미지로 저장, 사진 내 사람 수를 계산하는 모델입니다.

- 사용 모델: [YOLO v3](https://github.com/ultralytics/yolov3)
- 파일 경로 내 한글이 포함될 경우 잘 작동하지 않을 수 있습니다.
- yolov3/detect.py 파일의 아래 내용을 주석처리하고 실행시켜 주세요. 
```
# Print results
t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
```