import cv2
import math

def set_label(image, contour, label):
    x, y, w, h = cv2.boundingRect(contour)
    pt1 = (x,y)
    pt2 = (x+w, y+h)
    cv2.rectangle(image, pt1, pt2, (0,0,255), 2)

    text_y = max(y-5, 20)
    cv2.putText(image,label,(x,text_y), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,255), 1)

img = cv2.imread("./images/polygon.bmp")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# THRESH_BINARY : 기준값을 기준으로 기준값 보다 높으면 흰색. 낮으면 검정색
# THRESH_BINARY_INV : inverse. 기준값을 기준으로 기준값보다 높으면 검정색. 낮으면 흰색
_, img_bin = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

# 바깥 외곽선만 땀
contours, _ = cv2.findContours(img_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    area = cv2.contourArea(contour) # 면적 구하기

    if area < 50:
        continue

    # arcLength: 윤곽선의 길이. 둘레를 계산하는 함수
    # True: 폐곡선 여부
    perimeter = cv2.arcLength(contour, True) # 윤곽선 둘레 계산 #윤곽선 좌표를 넣으면 둘레를 구해줌. # tf는 시작점과 마지막점 연결 여부. 폐곡선
    #print(perimeter)

    # epsilon : 원본 윤곽선과 근사 윤곽선 사이의 최대 허용 거리
    # 원본 윤곽선을 얼마나 대충 따라가도 되는지(근사의 허용 정도)
    epsilon = 0.02 * perimeter
        
    """
    approxPolyDP()
    복잡한 윤곽선을 더 적은 수의 꼭짓점으로 근사
    """
    approx = cv2.approxPolyDP(contour, epsilon, True) # true는 폐곡선 여부
    # print(approx)
    vertex_count = len(approx)
    print("꼭짓점 수: ",vertex_count)

    if vertex_count == 3:
        set_label(img, contour, "TRIANGLE")
    elif vertex_count == 4:
        set_label(img, contour, "QUAD")
    else:
        if perimeter == 0:
            continue

        circularity = (4.0 * math.pi * area / (perimeter * perimeter)) # 원형도 계산. 1에 가가울수록 원에 가까움 # 1보다 작을수록 점점 길쭉한 원(타원)
        print("원형도: ",circularity)

        if circularity > 0.8:
            set_label(img, contour, "CIRCLE")
        else:
            set_label(img, contour, "OTHER")


cv2.imshow("binary",img_bin)
cv2.imshow("polygon result",img)

cv2.waitKey(0)
cv2.destroyAllWindows()