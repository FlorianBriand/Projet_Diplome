from PIL import Image
from pyzbar.pyzbar import decode


def detecteQRcode(image):
    decodeQR = decode(Image.open(image))
    if decodeQR == []:
        print("Aucun QR code n'a été détecté")
    decodeQR = decodeQR[0].data.decode("utf-8")
    print("Le QR code détecté est : " + decodeQR)
    return decodeQR
