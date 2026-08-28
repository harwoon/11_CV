import cv2
import sys

cap1 = cv2.VideoCapture("./movies/232538_tiny.mp4")
cap2 = cv2.VideoCapture("./movies/276624_tiny.mp4")

if not cap1.isOpened() or not cap2.isOpened():
    print('입력 동영상 중 하나 이상을 열 수 없습니다.')
    sys.exit()

# 붙일 떄는 해상도가 같아야 두 영상을 붙일 수 있다.
# 두 영상의 fps나 영상 길이가 다를 수 있으니 확인해 맞춰서 출력해야한다.

width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps1 = cap1.get(cv2.CAP_PROP_FPS)
fps2 = cap2.get(cv2.CAP_PROP_FPS)

print('너비: ',width)
print('높이: ',height)
print('FPS1: ', fps1)
print('FPS2: ',fps2)

# fourcc(Four Character code)
# 4개의 글자로 동영상 코덱을 지정하는 코드 -> 내부적으로 숫자로 바뀌어 압축 알고리즘을 알아냄
"""
이미지(영상): 1920 * 1080 * 3 byte = 6.2MB
1초에 30fps > 186MB
1분 > 11GB

코덱 / 동영상 포맷

.mp4, avi, mov, mkv .. : 컨테이너. 동영상 파일 포맷
H.264, H265, XVID, MJPEG, AVI : 코덱(압축하는 알고리즘)

movie.mp4
MP4 컨테이너
Video: H.264
Audio: AAC
자막 / 시간정보 등 ..

코덱의 종류
XVID, MJPG, H.264(H264), H.256/HEVC(H265), VP9, AV1


"""

# * unpacking(변수 앞에 쓰이면 언패킹의 의미) > 'x','v','i','d' : 각각의 정수값을 뽑아 알고리즘을 찾음
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("mix.avi", fourcc, fps1, (width, height)) # 알고리즘에 따라 포맷 정해짐

if not out.isOpened():
    cap1.release()
    cap2.release()
    raise RuntimeError('출력 동영상 파일을 생성할 수 없습니다.')

delay = max(1,round(1000/fps1))
stop = False

for cap in (cap1,cap2):
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame.shape[1] != width or frame.shape[0] != height: # 0: width 1:height
            frame = cv2.resize(frame, (width,height))
        out.write(frame)
        cv2.imshow('output',frame)
        if cv2.waitKey(delay) == 27:
            stop = True
            break
    if stop:
        break

cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()