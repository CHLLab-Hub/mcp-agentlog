import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("./data/images/Hawkes.jpg", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./data/images/field.bmp")

# equalizeHist(): 픽셀 밝기 분포를 재배치하여 전체적인 명암 대비를 향상시키는 데 사용
equalized_gray = cv2.equalizeHist(img_gray)

# 컬러 영상의 B, G, R 채널을 각각 따로 평활화하면 색 자체가 크게 변할 수 있음
# 밝기와 색상 정보를 분리할 수 있는 YCrCb로 변환한 뒤, Y(밝기) 채널에만 히스토그램 평활화를 적용
# Y: 밝기 정보, Cr: 빨강 계열 색차 정보, Cb: 파랑 계열 색차 정보
ycrcb = cv2.cvtColor(img_color, cv2.COLOR_BGR2YCrCb)
ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0]) # ycrcb[높이, 너비, 채널]
equalized_color = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

# nomalize(): 현재 최솟값과 최대값을 지정한 범위로 선형적으로 늘림 << equalize()와 비슷한 역할을 할 수 있음
normalized_gray = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX)

# 히스토그램 계산
hist_original = cv2.calcHist([img_gray], [0], None, [256], [0, 255])
hist_equalized = cv2.calcHist([equalized_gray], [0], None, [256], [0, 256])
hist_normalized = cv2.calcHist([normalized_gray], [0], None, [256], [0, 256])

cv2.imshow('gray original', img_gray)
cv2.imshow('gray equalized', equalized_gray)
cv2.imshow('gray normalized', normalized_gray)
cv2.imshow('color original', img_color)
cv2.imshow('color equalized', equalized_color)

histograms = { "original": hist_original, "equalized": hist_equalized, "normalized": hist_normalized}
plt.figure(figsize=(12, 4))

for i, (title, hist) in enumerate(histograms.items(), start=1):
    plt.subplot(1, 3, i)
    plt.plot(hist)
    plt.title(title)
    plt.xlim([0, 256])

plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()