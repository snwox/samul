import cv2
from module import licensePlate

img = cv2.imread('./test/1.jpg')
carNumber = licensePlate.detect(img)

print(carNumber)