import os
import time
import stegano as stg
import cv2
import qrcode

def detecteQRcode(image):
    d = cv2.QRCodeDetector()
    val, points, qrcode = d.detectAndDecode(cv2.imread(image))
    # si val est vide, il n'y a pas de QRcode
    if val:
        print("QRcode detecté")
    else:
        print("Pas de QRcode")

    return val
"""
if __name__ == '__main__':

    content = "RSA-SHA2-256(code.txt)= b67f623081c0adda7e585bf33e5b9cee01242b6147081c3505ab33098d60fb9695d968972f258983b46bfeb960cc6ccefe9d3e87bb544072c035b1f7f94d6746363023c5d67c07029c13d8f308d4d72165a30f03be684a2c433dacaa6c2addff3b5ff3206eba63f871444654d15b922b3aecdf49c93a879557b2aedf476bcca7253086d46c87f62842bf6df1b7c6b1bcb1fc97e25ca80c9eda77a5514cfb607a602eb1e01df283131360e57e948e9cce5ef2438c6ea7c827b5bf3a9b707d4233bb4ccc7ac761b42bd742c28791ff3eeccbc77e4bbb0c2f51fae66f16914609bd02faf702c657cf2eb4065b825626f7cc0a5a0b6f09f895a0aafa072a16979d9b"

    qr = qrcode.make(content)
    # Save the qr code as a png file
    qr.save("diplome/diplomeCree/C_R.png")

    image = 'diplome/diplomeCree/C_R.png'
    # vérifier que le fichier existe
    if not os.path.isfile(image):
        print("Le fichier n'existe pas")
        exit()
    signature = detecteQRcode(image)
    print("signature:", signature)
"""





