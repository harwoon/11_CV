import cv2

"""
연결 요소 라벨링(Connected Components Labeling)
이진 영상에서 서로 붙어 있는 흰색 픽셀 덩어리를 하나의 객체로 보고 번호를 붙이는 작업 (선수 이진화가 되어있어야함. 배경은 검은색, 객체는 흰색)
명확하게 구분하기 위해 이진화로 흑백으로 변환. 객체 간의 구분이 아닌 객체 구분이므로. 이게 빠름
"""

img = cv2.imread("./images/keyboard.bmp", cv2.IMREAD_GRAYSCALE)

_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) # 값은 알 필요없어 안받음.

dst = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

# cv2.connectedcomponentsWithStates()
# 라벨링을 수행하면서 객체에 대한 정보를 계산
# connectivity: 픽셀들이 어떤 방향으로 붙어 있으면 같은 객체로 판단할지를 결정. 4(상하좌우) or 8(상하좌우+대각)만 가능
# count: 전체 라벨 개수(안에 들어있는 객체 개수를 셈) 배경도 하나의 라벨로 인식
# labels: 원본 영상과 크기가 같은 2차원 배열이며, 각각의 픽셀이 몇 번 객체에 속하는지 저장
# stats: 각 객체의 위치와 크기 정보 [left, top, width, height, area]
# centroids: 각 객체의 중심 좌표
count, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bin, connectivity=8)
print("라벨 개수(배경 포함): ",count) # 38 개수가 안맞는 이유 -> 노이즈 존재
print("라벨 개수(배경 제외): ",count-1) # 37

print("labels shape: ", labels.shape) # 이미지와 동일
print("labels 일부: ", labels[:10, :10])

print("stats:")
print(stats)
"""
stats:
[[     0      0    512    512 256750] # 배경
 [   102     30     23     29    341]
 [   276     32     23     27    259]
 [   451     36      9     36    168]
 [   278     45      1      1      1] # 1픽셀짜리들이 노이즈
 [   102     95     21     33    230]
 [   274     97     21     34    373]
 [   445     99     21     34    366]
 [   387    149      1      1      1]
 [    16    198     34     38    350]
 [   189    200     29     38    452]
 [   370    201      8     38    221]
 [   197    253      1      1      1]
 [   271    258     14     40    245]
 [   441    260     14     40    239]
 [    78    272     36     25    313]
 [   135    310      1      1      1]
 [   302    312      1      1      1]
 [   470    314      1      2      2]
 [   121    320      1      1      1]
 [   247    320      1      1      1]
 [   283    331      1      1      1]
 [    60    365     29     37    469]
 [   231    366     20     37    265]
 [   398    366     30     38    470]
 [   344    394      1      1      1]
 [   344    407      1      3      3]
 [   191    411      1      1      1]
 [   314    413     13     35    213]
 [   179    418      1      2      2]
 [   344    418      1      1      1]
 [   481    430     12     34    184]
 [   126    440     35     22    213]
 [   178    448      1      1      1]
 [   270    461      1      1      1]
 [   509    473      1      1      1]
 [   174    477      1      1      1]
 [   509    476      1      1      1]]
"""

print("centroids:")
print(centroids)

for i in range(1, count):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]

    if area < 30:
        continue

    cx, cy = centroids[i] # 실수

    cv2.rectangle(dst, (x,y), (x+w, y+h), (0,255,255), 2)
    cv2.circle(dst, (int(cx), int(cy)), 3, (0,0,255), -1)

cv2.imshow("img",img)
cv2.imshow("bin",img_bin)
cv2.imshow("labeling result",dst)
cv2.waitKey(0)
cv2.destroyAllWindows()


