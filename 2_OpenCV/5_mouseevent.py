import cv2
import numpy as np

oldx = 0
oldy = 0

def on_mouse(event, x, y, flags, param ): #변수 순서 정해져있음
    """
    event : 발생한 마우스 이벤트 종류 객체
    x, y: 현재 마우스 좌표
    flag: 마우스 버튼/키 상태
    param: setMouseCallback()에서 전달할 추가 데이터
    """
    global oldx,oldy

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'왼쪽 버튼 DOWN: ({x},{y})')
        oldx,oldy = x,y
    elif event == cv2.EVENT_LBUTTONUP:
        print(f'왼쪽 버튼 UP: ({x},{y})')
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print(f'드래그 중: ({x},{y})')
            cv2.line(img,(oldx,oldy),(x,y),(255,51,255),3)
            oldx,oldy = x,y
            cv2.imshow("canvas",img)


img = np.full((500,500,3),255,dtype=np.uint8) # 이미지가 그레이스케일이면 컬러로 덮어쓸 수 없음: shape이 안맞음

cv2.rectangle(img, (50, 200), (200,300), (0,255,0), 3  ) #(도화지)(왼쪽 위 모서리 좌표) (오른쪽 아래 모서리) (색상) (두께)
cv2.rectangle(img, (300,200), (400,300),(0,255,0),-1) # -1은 채우기

cv2.circle(img,(150,400),50,(255,0,0),3)
cv2.putText(img, "Hello",(50,100), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0,0,0), 1) #글자, 폰트, 크기, 색, 두께

cv2.imshow("canvas",img)
cv2.setMouseCallback("canvas",on_mouse)

cv2.imshow("canvas",img)
cv2.waitKey(0)
cv2.destroyAllWindows()