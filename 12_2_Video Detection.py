### 모델을 불러와서 웹캠에서 실행해봅시다. 
# https://docs.ultralytics.com/modes/predict/#streaming-source-for-loop

# 비디오를 연동할 때는 opencv를 사용합니다. 
# https://opencv.org/

# 파이썬 버전은 아래와 같이 설치하면 됩니다. 
# pip install opencv-python

import cv2
from ultralytics import YOLO

# 모델 불러오기
model = YOLO('yolov8n.pt')

# 비디오 파일 열때
# video_path = "path/to/your/video/file.mp4"
# cap = cv2.VideoCapture(video_path)

# Webcam 사용 시
cap = cv2.VideoCapture(0)  # Device 번호이며, 0번 부터 부여

# 비디오를 이미지 단위로 불러들여서 처리합니다. 
while cap.isOpened():  # 영상이 들어올 때
    
    # 프레임 단위로 읽습니다. 
    success, frame = cap.read()  # 정상적으로 들어오는지와, 이미지입니다. 

    if success:  # 정상적으로 들어온 경우에
    
        # 모델에 프레임을 넣고, Object Detection을 합니다. 
        results = model(frame)

        # Yolo에서 제공하는 함수를 통해 디텍션 결과를 이미지로 저정합니다. 
        annotated_frame = results[0].plot()

        # 저장 결과를 출력합니다. 
        cv2.imshow("YOLOv8 Inference", annotated_frame)

        # 'q'를 누르면 실행이 멈추도록 합니다. 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # 프레임이 들어오지 않으면 루프를 벗어나게 합니다. 
        break

# 연결을 종료하고, 창을 닫습니다. 
cap.release()
cv2.destroyAllWindows()