import cv2
import numpy as np

img_gray = cv2.imread("./2_OpenCV/images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./2_OpenCV/images/dog.bmp", cv2.IMREAD_COLOR)

print('img_gray type: ', type(img_gray)) #img_gray type:  <class 'numpy.ndarray'>
print('img_gray shape: ', img_gray.shape) #img_gray shape:  (364, 548)
print('img_gray dtype: ', img_gray.dtype) #img_gray shape:  uint8

print('img_color type: ', type(img_color)) #img_color type:  <class 'numpy.ndarray'>
print('img_color shape: ', img_color.shape) #img_color shape:  (364, 548, 3)
print('img_color dtype: ', img_color.dtype) #img_color dtype:  uint8

h, w = img_color.shape[:2] # (364, 548, 3)을 슬라이싱 해서 가져옴
print(f'이미지 크기: {w}*{h}') # 이미지 크기: 548*364

if img_color.ndim == 3:
    print('img_color는 컬러 이미지입니다.')

elif img_color.ndim == 2: # 1이 아님을 유의
    print('img_color는 그레이스케일 이미지입니다.')

img1 = np.zeros((240, 320, 3), dtype=np.uint8 ) #0으로 다 채우니 검은 이미지 # 가로 320, 세로 240, 컬러(검은색)
#np.empty(): 메모리 공간만 할당하고 예측할 수 없는 값을 저장함
img2 = np.empty((240, 320), dtype=np.uint8) # 색상값 안줘서 자동으로 그레이스케일
img3 = np.full((240,320),120, dtype=np.uint8) #모든 픽셀을 120으로 채움

cv2.imshow('zeros',img1)
cv2.imshow('empty',img2)
cv2.imshow('full_120',img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

