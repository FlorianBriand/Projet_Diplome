import cv2



def detecteQRcode(image):
    d = cv2.QRCodeDetector()
    val, points, qrcode = d.detectAndDecode(cv2.imread(image))
    # si val est vide, il n'y a pas de QRcode
    if val:
        print("QRcode detecté")
        print("Valeur:", val)
        print("Points:", points)
        print("QRcode:", qrcode)
    else:
        print("Pas de QRcode")
    return val

def takePicture():
    webcam = cv2.VideoCapture(0)
    # Check if the webcam is opened correctly
    if not webcam.isOpened():
        raise IOError("Cannot open webcam")
    # Read the webcam
    ret, frame = webcam.read()
    # Save the webcam image
    cv2.imwrite('webcam.png', frame)
    webcam.release()

if __name__ == '__main__':
    takePicture()
    while not detecteQRcode('webcam.png'):
        takePicture()


