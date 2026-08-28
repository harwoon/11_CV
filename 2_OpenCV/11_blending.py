import cv2
import matplotlib.pyplot as plt

img1 = cv2.imread('./images/man.jpg')
img2 = cv2.imread('./images/turkey.jpg')

# 이미지 크기가 다르면 블렌딩 불가
if img1.shape != img2.shape:
    raise ValueError(f'두 이미지의 shape가 다릅니다: {img1.shape}, {img2.shape}')

dst_numpy = img1 + img2 # ndarray의 덧셈
dst_opencv = cv2.add(img1, img2)

images = {"img1":img1, "img2":img2, "numpy":dst_numpy, "cv2.add":dst_opencv}

plt.figure(figsize=(10,8))
for i, (title,image) in enumerate(images.items(),start=1):
    plt.subplot(2,2,i)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis('off')
plt.tight_layout()
plt.show()