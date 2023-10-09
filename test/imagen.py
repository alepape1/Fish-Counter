import cv2
import numpy as np

img = cv2.imread('tiger.jpg',0)
kernel = np.ones((2,2     ),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 1)

cv2.imshow("Imagen", img)
cv2.imshow("kernel", kernel)
cv2.imshow("erosion", erosion)
# Esperar a que se presione una tecla para cerrar la ventana
cv2.waitKey(5000)

# Cerrar todas las ventanas
cv2.destroyAllWindows()

print(img)
print(kernel)
