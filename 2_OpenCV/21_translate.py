import cv2
import numpy as np

img = cv2.imread("./images/dog.bmp")

h, w = img.shape[:2]

# 이동(translation) 픽셀을 이동시킨다.

"""
2 * 3 이동 변환 행렬
[ 1 0 tx]
[ 1 0 ty]
tx = x 축 이동 거리
ty = y 축 이동 거리
"""
aff_translate = np.array([
    [1, 0, 150],
    [0, 1, 100]
], dtype=np.float32)

dst_translate = cv2.warpAffine(img, aff_translate, (w,h)) # 어떤 행렬 변환을 일으킬지 알려줌 # 이미지, 변환, 내보낼 크기(튜플)

# 크기 변경(Resize)
# 보간(Interpolation): 이미 알고 있는 주변 값들을 이용해서 중간에 필요한 값을 추정하는 것
# INTER_NEAREST: 최근접 이웃. 가장 가까운 픽셀 사용(가중 평균 이용해 선형적으로 계산)
# INTER_LINEAR: 선형 보간. 주변 픽셀을 이용해서 계산(속도가 빠름.그러나 주변을 선형계산해서 사용해서)
# INTER_CUBIC: 3차 보간. 더 넓은 주변 픽셀을 이용해 부드럽게 계산(더 세밀하게 보지만 속도가 느려짐)
# INTER_AREA: 영역 보간. 축소할 때 주로 사용
dst_nearest = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_NEAREST) # 픽셀 개수를 늘리거나 줄여 해상도 조절
dst_cubic = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_CUBIC)

# 회전(Rotation)
center = (w/2, h/2)
# getRotationMatrix2D(회전 중심좌표, 회전 각도, 확대/축소 비율)
# 회전 각도는 양수일 경우 반시계 방향
rot_matrix = cv2.getRotationMatrix2D(center, 30, 0.7) # 중심 포인트, 반시계방향 몇 도 돌릴지, 확대/축소 비율
dst_rotate = cv2.warpAffine(img, rot_matrix, (w,h))


cv2.imshow("original", img)
cv2.imshow("translate",dst_translate)
cv2.imshow("dst_nearest",dst_nearest)
cv2.imshow("dst_cubic",dst_cubic)
cv2.imshow("dst_rotate",dst_rotate)

cv2.waitKey(0)
cv2.destroyAllWindows()