import cv2
import numpy as np

cap = cv2.VideoCapture('video_files\pez1.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))

# Lista de objetos de seguimiento
trackers = []

while True:

    ret, frame = cap.read()
    if ret == False: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Dibujamos un rectángulo en frame, para señalar el estado
    # del área en análisis (movimiento detectado o no detectado)
    cv2.rectangle(frame,(0,0),(frame.shape[1],40),(0,0,0),-1)
    color = (0, 255, 0)
    texto_estado = "Estado: No se ha detectado movimiento"

    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[0,40], [720,40], [720,450], [450,720]])

    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(gray, gray, mask=imAux)

    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=2)

    # Lista de objetos detectados
    objects = []

    # Encontramos los cotnornos presentes en fgmask, para luego basándonos
    # en su área poder determinar si existe movimiento
    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    for cnt in cnts:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            objects.append((x,y,x+w,y+h))

    # Crear un tracker para cada objeto nuevo
    for obj in objects:
        tracker = cv2.TrackerCSRT_create()
        tracker.init(frame, (obj[0], obj[1], obj[2]-obj[0], obj[3]-obj[1]))
        trackers.append(tracker)

    # Mostrar el número de objetos detectados en cada cuadro de video
    texto_num_obj = f"Número de objetos: {len(trackers)}"
    cv2.putText(frame, texto_estado, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    cv2.putText(frame, texto_num_obj, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # Mostrar el cuadro actual
    cv2.imshow('frame', frame)

    # Salir con ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
