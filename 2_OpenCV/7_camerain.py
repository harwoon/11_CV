import cv2
import sys

cap = cv2.VideoCapture(0) # 0은 기본 웹캠

if not cap.isOpened():
    print('카메라를 열 수 없습니다.')
    sys.exit()

print('카메라 연결 성공!')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

print('너비: ',width)
print('높이: ',height)
print('FPS: ',fps)

while True:
    ret, frame = cap.read() # ret: 이미지 가져올 수 있는지 #frame: 이미지 한 장 가져오기

    if not ret:
        print('카메라 프레임을 읽지 못했습니다.')
        break

    cv2.imshow('camera',frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()