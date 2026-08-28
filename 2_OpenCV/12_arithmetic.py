import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread("./images/dog.jpg")
img2 = cv2.imread("./images/square.bmp")

# 1. 단순 덧셈. 255보다 큰 값은 255로 제한
dst_add = cv2.add(img1, img2) # 흰색은 255라 더해도 255 유지. 검정은 0이라 영향없음. -> 가운데 흰 네모

# 2. 가중치 합성
# img1 * 0.5 + img2 * 0.5 + ?(추가로 넣고 싶은 값)
dst_blend = cv2.addWeighted(img1,0.5,img2,0.5,0) # 기본적으로 어두워짐. 여전히 검정은 0이라 영향 없음. 강아지만 어두워지는데, 흰 네모 부분 탓에 가운데가 밝음

# 3. 뺄셈. 음수가 되는 값은 0으로 제한
dst_subtract = cv2.subtract(img1,img2) # 0빼도 의미없어 테두리는 변화X. 가운데 흰색 빼서 검정임

# 4. 절대 차이
# |img1 - img2|
# 두 영상에서 픽셀값이 얼마나 다른지 확인할 때 사용 # 0을 빼서 테두리는 변화X. 절대값을 취해 반전되어 보임.
dst_absdiff = cv2.absdiff(img1,img2)

images = {"add":dst_add,"blend":dst_blend, "subtract":dst_subtract,"absdiff":dst_absdiff}

plt.figure(figsize=(10,8))
for i, (title,image) in enumerate(images.items(),start=1):
    plt.subplot(2,2,i)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
plt.tight_layout()
plt.show()