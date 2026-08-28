import cv2

"""
OpenCV의 산술 연산
이미지의 각 픽셀 값에 일정 값을 더하거나 빼는 방식으로 밝기를 조절할 수 있음
"""

img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)
bright_gray = cv2.add(img_gray, 100) # 0~255 : 0은 검정 255는 흰색
bright_color = cv2.add(img_color, 100)

# 나눗셈을 제외한 애들은 255를 넘어설 수 있음 / 값을 0~255로 제한함(초과될 수 없음)
dark_gray = cv2.subtract(img_gray, 100)
dark_color = cv2.subtract(img_color, 100)
multiply_gray = cv2.multiply(img_gray,2)
divide_gray = cv2.divide(img_gray,2)

cv2.imshow('gray', img_gray)
cv2.imshow('color',img_color)
cv2.imshow('bright_gray',bright_gray)
cv2.imshow('bright_color',bright_color)
cv2.imshow('dark_gray',dark_gray)
cv2.imshow('dark_color',dark_color)
cv2.imshow('multiply_gray',multiply_gray)
cv2.imshow('divide_gray',divide_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()