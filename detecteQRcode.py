import cv2

d = cv2.QRCodeDetector()

val, points, qrcode = d.detectAndDecode(cv2.imread("unknown.png"))

print(val)