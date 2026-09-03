import cv2
import numpy as np

"""
라벨링 - 객체를 면적으로 사각형 내부를 봄
윤곽선 - 객체의 외곽선
"""

"""
윤곽선(Contour)
객체의 바깥 경계선을 이루는 좌표들의 집합
"""

img = cv2.imread("./images/contours.bmp", cv2.IMREAD_GRAYSCALE)
milkdrop = cv2.imread("./images/milkdrop.bmp", cv2.IMREAD_GRAYSCALE)

_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
_, milk_bin = cv2.threshold(milkdrop, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

"""
cv2.findContours(image, mode, method)
mode: 윤곽선 사이의 부모/자식 관계를 어떻게 가져올지 설정
    
윤곽선의 계층 구조 (구멍 뚫린 객체일 때 바깥을 부모, 안을 자식으로 봄)
    RETR_EXTERNAL: 바깥 윤곽선만 반환
    RETR_CCOMP: 바깥 윤곽선과 내부 윤곽선을 모두 반환
    RETR_LIST: 부모-자식 관계를 중요하게 관리하지 않고 모든 윤곽선을 반환
    RETR_TREE: 모든 윤곽선을 반환하며 부모-자식 관계까지 전체 구조를 보존
method: 경계 좌표를 얼마나 자세하게 저장할 것인지 설정(CHAIN_APPROX_SIMPLE, CHAIN_APPROX_NONE)

contours: 모든 윤곽선. 하나의 좌표가 아니라 여러 좌표의 집합 ex) (10,13) (20,26) ....
          len(contours) > 찾은 윤곽선의 개수

RETR_CCOMP: 바깥 윤곽선과 내부 윤곽선을 모두 반환
CHAIN_APPROX_SIMPLE: 윤곽선 경계의 중간 좌표들을 줄임 (직선 그을 수 있는 건 중간좌표를 생략하고 그음. 메모리 절약 가능)
hierarchy: 윤곽선끼리의 관계를 저장. 예) [2, -1, 1, -1] next(다음 윤곽선), previous(이전 윤곽선), first_child(자식 윤곽선), parent(부모 윤곽선)
"""

contours, hierarchy = cv2.findContours(img_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
milk_contours, milk_hierarchy = cv2.findContours(milk_bin, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

print("contours 개수: ",len(contours))
print("milk contours: ", len(milk_contours))

print("hierarchy: ")
print(hierarchy)

dst = cv2.cvtColor(img_bin, cv2.COLOR_GRAY2BGR)
cv2.drawContours(dst,contours,-1,(0,0,255),2)

h, w = milk_bin.shape[:2]
dst_milk = np.zeros((h,w,3), dtype=np.uint8)

for i,contour in enumerate(milk_contours):
    color = ((37*i)%256, (97*i)%256, (174*i)%256)
    cv2.drawContours(dst_milk, milk_contours, i, color, 2)

cv2.imshow("img_bin", img_bin)
cv2.imshow("dst",dst)
cv2.imshow("milk_bin",milk_bin)
cv2.imshow("dst_milk",dst_milk)

cv2.waitKey(0)
cv2.destroyAllWindows()
