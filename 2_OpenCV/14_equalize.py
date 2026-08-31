import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("./images/Hawkes.jpg", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/field.bmp")


"""
색분리에 RGB만 있는 것이 아님

YCrcb
- 컬러 이미지를 표현하는 또 다른 색 공간
- 밝기와 색상 정보를 분리해서 저장
- Y: 밝기 정보(숫자로), Cr(붉은 성향 red), Cb(푸른 성향 blue) (두 개 더하거나 빼면 초록 나옴): 색상 정보
"""

ycrcb = cv2.cvtColor(img_color, cv2.COLOR_BGR2YCrCb) #색상 포맷 바꾸기
ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0]) #색상의 밝기 정보만 equalize
equalized_color = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

"""
50~150에만 몰려있는 픽셀들을 가진 사진을 0~255로 맞춤 : 전체적인 픽셀 정보가 비율에 맞게 늘어남. contrast stretching(대비 스트레칭)
픽셀이 몰려있으면 뚜렷하게 보이지 않음.

normalize()
- 정규화
- 값의 범위 조정
- 최솟값 / 최댓값 (최소 최대값에 맞춰 늘림)
- 기본적으로 비율을 유지하며 변화

- 대비 개선이 주목적은 아님
- 데이터 범위 통일. 시각화. 전처리 (주목적)

"""
normalized_gray = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX) # 영상, 내보낼 크기(안넣으면 입력과 크기 동일), min, max(min~max범위로 늘리기), 상수

"""
equalizeHist()
- 히스토그램 평활화
- 대비 향상(목적)
- 픽셀들의 분포(기준) (30에 몇 개 등. 누적분포를 계산해서 퍼트리는 식으로)
- 일반적으로 0~255 범위를 늘려줌
- 대비 개선에 특화된 함수

"""

equalized_gray = cv2.equalizeHist(img_gray)

hist_original = cv2.calcHist([img_gray],[0], None, [256], [0,256])
hist_equalized = cv2.calcHist([equalized_gray],[0], None, [256], [0,256])
hist_normalized = cv2.calcHist([normalized_gray],[0], None, [256], [0,256])

cv2.imshow("gray original",img_gray) # 그냥 띄우니 사진이 뿌옇다
cv2.imshow("color original", img_color)
cv2.imshow("gray nomralized", normalized_gray) # constrast stretching 후 사진이 또렷해짐
cv2.imshow("equalized gray", equalized_gray)
cv2.imshow("color equalized", equalized_color)

plt.figure(figsize=(12,4))
histograms = {'original': hist_original, 'equalized': hist_equalized, 'normalized': hist_normalized}

for i, (title, hist) in enumerate(histograms.items(), start=1):
    plt.subplot(1,3,i)
    plt.plot(hist)
    plt.title(title)
    plt.xlim([0,256])
plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

"""
색 변화가 큰 것은 객체의 테두리
-> 테두리를 극명하게 만들기 위해 대비가 필요함
"""