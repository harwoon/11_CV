import cv2
import numpy as np

img = cv2.imread("./images/sudoku.jpg", cv2.IMREAD_GRAYSCALE)

# 전역 Otsu 이진화
otsu_threshold, global_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print("otsu_threshold: ", otsu_threshold)

# 지역 Otsu 이진화
# 지역마다 서로 다른 자동 임계값을 사용함
# 전체 이미지를 4x4로 쪼개서 각 구역을 이진화
"""
내가 푼 예제
img_copy = img.copy()
h, w = img.shape[:2]

for width in range(0,w, int(w/4)):
    for hegiht in range(0,h,int(h/4)):
        local_threshold,local_otsu = cv2.threshold(img_copy[hegiht:hegiht+int(h/4),width:width+int(w/4)],0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_copy[hegiht:hegiht+int(h/4),width:width+int(w/4)] = local_otsu
"""

local_otsu = np.zeros_like(img)
rows = 4
cols = 4

# np.linspace()
# 시작값부터 끝값까지 일정한 간격으로 원하는 개수만큼 숫자를 만들어주는 함수
# np.linspace(start, stop, num(몇 개를 만들지. 간격x))
y_edges = np.linspace(0, img.shape[0], rows+1, dtype=int)
x_edges = np.linspace(0, img.shape[1], rows+1, dtype=int)

for row in range(rows):
    for col in range(cols):
        y1 = y_edges[row]
        y2 = y_edges[row+1]
        x1 = x_edges[col]
        x2 = x_edges[col+1]
        block = img[y1:y2, x1:x2]

        _, block_binary = cv2.threshold(block, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        local_otsu[y1:y2, x1:x2] = block_binary

# 적응형 이진화
# adaptiveThreshold(): 픽셀마다 주변 영역을 보고 임계값을 계산
# adaptiveThreshold(img, maxValue, blockSize(주변 픽셀을 얼마나 볼 것인지. 3이상 홀수), C(값을 조절할 수 있는 상수))
# maxValue: 조건을 만족한 픽셀에 넣을 값, blockSize: 주변 영역의 크기. 반드시 3 이상의 홀수, C: 계산된 주변 기준값에서 빼는 상수
# T = 주변 평균(또는 가중 평균) - C
# C가 커지면 T가 낮아지므로 같은 영상에서는 흰색으로 판정되는 픽셀이 더 많아질 수 있음
block_size = 9
C = 5
# 주변 픽셀의 단순 평균을 기준으로 사용
# 노이즈 존재
adaptive_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

# 주변 픽셀에 Gaussian 가중치를 적용한 평균을 기준으로 사용
# 주변 픽셀은 가중치를 크게 주고, 먼 픽셀은 가중치를 작게 주는 방식 => 노이즈 제거 효과 있음(나중에 먼지같은거 제거할 때도 사용)
adaptive_Gaussian = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)

cv2.imshow("original",img)
cv2.imshow("global_otsu",global_otsu) # 자동 이진화하니 왼쪽 밑이 어두워 그림이 안보임
#cv2.imshow("local_otsu",img_copy)
cv2.imshow("local_otsu", local_otsu)
cv2.imshow("adaptive_mean", adaptive_mean)
cv2.imshow("adaptive_Gaussian", adaptive_Gaussian)

cv2.waitKey(0)
cv2.destroyAllWindows()