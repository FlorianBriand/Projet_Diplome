import time
import stegano as stg
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
"""
if __name__ == '__main__':
    image = 'diplome/diplomeCree/qr_code.png'
    signature = detecteQRcode(image)
    # verification de la signature
    # os.system("openssl dgst -sha256 -verify ca.pem -signature sha1.sign test.txt")

    # Utilisation de la fonction récupérer pour récupérer le message
    message = stg.recuperer("diplome/diplomeCree/stegano_Briand_Flo.png", 80)
    # enelever les étoiles
    message = message.replace("*", "")
    print("Message : ", message)
"""





