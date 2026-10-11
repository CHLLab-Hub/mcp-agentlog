import cv2
import sys

cap = cv2.VideoCapture('./data/movies/232538_tiny.mp4')

if not cap.isOpened():
    print('동영상을 불러올 수 없습니다.')
    sys.exit()
print('동영상 로드 성공')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print('가로:', width)
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print('세로:', height)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print('전체 프레임:', frame_count)
fps = cap.get(cv2.CAP_PROP_FPS)
print('FPS:', fps)

# FPS를 이용해 프레임 사이 대기 시간을 계산하여 자연스러운 동영상 실행, FPS는 동영상이 1초당 몇 장면이 재생된다는 정보일 뿐이라 delay를 통해 재생속도를 맞춰줘야 함
# 예시) 30FPS라면 1초에 30장을 보여주므로 약 33ms마다 한 프레임을 표시함
delay = max(1, round(1000/ fps)) if fps > 0 else 33

while True:
    """
    ret: 프레임을 정상적으로 읽었는지 여부; boolean
    frame: 읽어온 한 장의 영상 프레임
    """
    ret, frame = cap.read()
    
    if not ret: # 영상 끝에 도달하거나 읽기에 실패하면 ret=False가 됨
        break

    cv2.imshow("frame", frame)
    
    if cv2.waitKey(delay) == 27:
        break

cap.release()
cv2.destroyAllWindows()