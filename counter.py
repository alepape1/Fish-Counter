import cv2
import numpy as np

def detect_motion(frame, detected_fish, fish_count):

    frame = cv2.resize(frame, (360, 240))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.rectangle(frame, (0, 0), (frame.shape[1], 40), (0, 0, 0), -1)
    color = (0, 255, 0)
    texto_estado = "Estado: No se ha detectado movimiento"

    area_pts = np.array([[0, 40], [720, 40], [720, 450], [0, 450]])

    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            if (x, y, w, h) not in detected_fish:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                texto_estado = "Estado: ALERTA Movimiento Detectado!"
                color = (0, 0, 255)
                fish_count += 1
                detected_fish.append((x, y, w, h))

    cv2.drawContours(frame, [area_pts], -1, color, 2)
    cv2.putText(frame, texto_estado , (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color,2)
    cv2.putText(frame, "Peces detectados: " + str(fish_count), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),1)
    cv2.imshow('fgmask', fgmask)
    cv2.imshow("frame", frame)

    # Resto del código de procesamiento (sin el bucle while)

    return frame


print("Versión de OpenCV instalada:", cv2.__version__)
cap = cv2.VideoCapture('video_files\pez1.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
max_detect = 0

fish_count = 0
detected_fish = []  # Lista para realizar un seguimiento de los peces detectados

while True:
    ret, frame = cap.read()
    if ret == False: break

    detect_motion(frame, detected_fish, fish_count)
    print(f"Peces detectados {fish_count}")

    k = cv2.waitKey(70) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
