import cv2
import numpy as np

# 이전 마우스 좌표 저장
oldx = 0
oldy = 0

def on_mouse(event, x, y, flags, param):
    """
    event: 발생한 마우스 이벤트 종류
    x, y: 현재 마우스 좌표
    flags: 마우스 버튼/키 상태
    param: setMouseCallback()에서 전달할 추가 데이터
    """
    global oldx, oldy

    if event == cv2.EVENT_LBUTTONDOWN: 
        print(f'왼쪽 버튼을 누른 좌표: ({x}, {y})')
        oldx, oldy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if flags & cv2.EVENT_FLAG_LBUTTON:
            print(f'드래그 중: ({x}, {y})')
            cv2.line(img, (oldx, oldy), (x, y), (255, 51, 255), 3) # line(이미지, 좌표1, 좌표2, 색상, 두께)
            oldx, oldy = x, y
            cv2.imshow("canvas", img)
    elif event == cv2.EVENT_LBUTTONUP:
        print(f'왼쪽 버튼 땐 좌표: ({x}, {y})')

# 흰색 배경 이미지 생성
img = np.full((500, 500, 3), 255, dtype=np.uint8)

# canvas 창에서 발생하는 모든 마우스 이벤트를 on_mouse()가 처리하도록 연결
cv2.namedWindow("canvas")

# rectangle(이미지, 왼쪽 위 좌표, 오른쪽 아래 좌표, 색상, 두께)
cv2.rectangle(img, (50, 200), (200, 300), (0, 255, 0), 3)
cv2.rectangle(img, (300, 200), (450, 300), (0, 255, 0), -1) # -1: 내부를 색으로 채움

# circle(이미지, 센터 좌표, 반지름, 색상, 두께)
cv2.circle(img, (150, 400), 50, (255, 0, 0), 3)

# putText(이미지, 문장, 좌표, 폰트, 크기, 색상, 두께)
cv2.putText(img, "Hello", (50, 100), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)

cv2.imshow("canvas", img)
cv2.setMouseCallback("canvas", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindow