import cv2
import numpy as np
# 사진 모서리 사용자가 맞춰서 변환하기

"""
내가 짠 예제 코드
img = cv2.imread("./images/namecard.jpg")

dst_w = 600
dst_h = 400

idx = 0
is_dragging = False
color = (255, 0, 0)

src_quad = np.array([
    [50,50],
    [700,50],
    [700,920],
    [50,920]
], dtype=np.float32)

dst_quad = np.array([
    [0,0],
    [dst_w-1, 0],
    [dst_w-1, dst_h-1],
    [0, dst_h-1]
], dtype=np.float32)

preview = img.copy()
for pt in src_quad.astype(int):
    cv2.circle(preview, tuple(pt), 8, (0,0,255), -1)

cv2. polylines(preview, [src_quad.astype(np.int32)], True, (0,255,0),3)

def on_mouse(event, x, y, flags, param):
    global idx, is_dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        is_dragging = True
        for i, pt in enumerate(src_quad):
            dx = pt[0] - x
            dy = pt[1] - y
            if abs(dx) < 15 and abs(dy) < 15:   # x좌표 차이, y좌표 차이가 둘 다 15px 이내면 선택
                idx = i
                break

    elif event == cv2.EVENT_MOUSEMOVE and is_dragging:
        preview = img.copy()
        src_quad[idx] = [x,y]

        for pt in src_quad.astype(int):
            cv2.circle(preview, tuple(pt), 8, (0,0,255), -1)

        cv2. polylines(preview, [src_quad.astype(np.int32)], True, (0,255,0),3)

        cv2.imshow("img", preview)

    elif event == cv2.EVENT_LBUTTONUP and is_dragging:
        is_dragging = False
        preview = img.copy()
        src_quad[idx] = [x,y]

        for pt in src_quad.astype(int):
            cv2.circle(preview, tuple(pt), 8, (0,0,255), -1)

        cv2. polylines(preview, [src_quad.astype(np.int32)], True, (0,255,0),3)

        cv2.imshow("img", preview)

cv2.imshow("img",preview)
cv2.setMouseCallback("img",on_mouse)

while True:
    key = cv2.waitKey(0)

    if key in (ord("i"),ord("I")):
        perspective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)
        dst = cv2.warpPerspective(img, perspective_matrix, (dst_w, dst_h))
        cv2.imshow("perspective result", dst)

    else:
        break

cv2.destroyAllWindows()
"""
def draw_roi(image, corners):
    preview = image.copy()
    point_color = (192, 192, 255)
    line_color = (128, 128, 255)

    for pt in corners:
        cv2.circle(preview, tuple(pt.astype(int)), 12, point_color, -1) # -1로 원에 색상을 채움

    for i in range(4):
        pt1 = tuple(corners[i].astype(int))
        pt2 = tuple(corners[(i+1)%4].astype(int))
        cv2.line(preview,pt1,pt2,line_color,2)

    return preview


def on_mouse(event, x, y, flags, param):

    global src_quad, drag_src

    if event == cv2.EVENT_LBUTTONDOWN:
        # 꼭짓점에 찍은 원을 끌어야 클릭이 되도록
        for i in range(4): # 네 꼭짓점 체크
            # 두 점 사이의 직선거리
            distance = cv2.norm(src_quad[i] - np.array([x,y], dtype=np.float32)) # norm : 두 벡터 간 거리를 구함. 기본적으로 유클리드 거리를 구함 sqrt( x**2 + y**2)

            if distance < 20:
                drag_src[i] = True
                break

    elif event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if drag_src[i]:
                # 좌표가 이미지 바깥으로 나가지 않도록 제한
                new_x = np.clip(x, 0, w-1) # 좌표가 이미지를 벗어나지 않도록
                new_y = np.clip(y, 0, h-1)
                src_quad[i] = (new_x,new_y)
                preview = draw_roi(img, src_quad)
                cv2.imshow("img",preview)
                break

    elif event == cv2.EVENT_LBUTTONUP:
        drag_src = [False, False, False, False]

img = cv2.imread("./images/namecard.jpg")

h,w = img.shape[:2]

dst_h = 500
dst_w = round(dst_h * 297/210) # a4용지 비율대로

# 왼쪽 위, 왼쪽 아래, 오른쪽 아래, 오른쪽 위
src_quad = np.array([
    [30, 30], # 좌측 상단
    [30, h-30], # 좌측 하단
    [w-30, h-30], # 우측 하단
    [w-30, 30] # 우측 하단
], dtype= np.float32)

# src_quad와 꼭짓점 순서가 맞아야 코딩이 편리
dst_quad = np.array([
    [0,0],
    [0, dst_h-1],
    [dst_w-1,dst_h-1],
    [dst_w-1,0]
],dtype=np.float32)

drag_src = [False, False, False, False]


display = draw_roi(img, src_quad) # 이미지와 좌표 넣기


cv2.imshow("img",display)
cv2.setMouseCallback("img",on_mouse)

print("네 꼭짓점을 드래그하여 영역을 맞추세요.")
print("Enter: 투시 변환")
print("ESC: 종료")

while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        raise SystemExit

    elif key in (10,13):
        break

perspective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)
dst = cv2.warpPerspective(img, perspective_matrix, (dst_w, dst_h), flags=cv2.INTER_CUBIC) # flags에 interpolation 줄 수 있음
cv2.imshow("perspective result",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()