import pyautogui
import cv2
import numpy as np
import time
from ultralytics import YOLO

# Load a model
model = YOLO("./yolov8n.yaml")  # build a new model from scratch
model = YOLO("./yolov8n.pt")  # load a pretrained model (recommended for training)

# 擷取螢幕的當前畫面
image = pyautogui.screenshot()
width = image.size[0]
height = image.size[1]

pTime = 0
cTime = 0
print("width:", width, "height:", height)
print("image mode:",image.mode)
while True:
    img_rgb = pyautogui.screenshot() #擷取大小畫面(x1,y1,x2,y2) 若要改成全螢幕ImageGrab.grab()
    img =np.array(img_rgb)
    # 將圖片轉換為 OpenCV 的 cv2.Mat 物件
    cv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = model(
        source=cv_image,
        mode="predict",
        classes=0,
        hide_labels=True,
        hide_conf=True,
        device=0
    )
    boxes = results[0].plot(
        hide_labels=True,
        hide_conf=True
    )

    cTime = time.time()#現在的時間
    fps = 1/(cTime-pTime)#換算FPS
    pTime = cTime

    cv_image= cv2.resize(boxes,(int(width*0.5),int(height*0.5)))     
    cv2.putText(cv_image, f"FPS : {int(fps)}",  (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)#把FPS畫在圖上
    cv2.imshow('oxxostudio', cv_image)
    if cv2.waitKey(1) == ord('q'):
        break
cv2.destroyAllWindows()

