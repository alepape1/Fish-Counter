import cv2

# Crea un objeto tracker
tracker = cv2.TrackerKCF_create()

# Abre el video
video = cv2.VideoCapture("test3.avi")

# Lee el primer frame
success, frame = video.read()

# Selecciona un objeto para rastrear haciendo clic en el video
bbox = cv2.selectROI("Seleccione el objeto a rastrear", frame, fromCenter=False, showCrosshair=True)

# Inicializa el tracker con el primer frame y la región de interés (ROI)
tracker.init(frame, bbox)

# Bucle sobre los frames del video
while True:
	# Lee el siguiente frame
	success, frame = video.read()

	# Si el video termina, termina el bucle
	if not success:
		break

	# Actualiza el tracker
	success, bbox = tracker.update(frame)

	# Si el tracker pierde la pista, termina el bucle
	if not success:
		print("lost")

	# Dibuja un rectángulo alrededor del objeto rastreado
	p1 = (int(bbox[0]), int(bbox[1]))
	p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
	cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

	# Muestra el frame actualizado
	cv2.imshow("Seguimiento de objetos", frame)

	# Si se presiona la tecla "q", termina el bucle
	if cv2.waitKey(1) & 0xFF == ord("q"):
		break

# Libera la captura de video y cierra todas las ventanas
video.release()
cv2.destroyAllWindows()
