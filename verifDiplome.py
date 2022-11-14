import os
import detecteQRcode as dQRC
import stegano as stg
from PIL import Image
def verifDiplome(filename):
    # Decrypter la stegano
    #localisation du fichier
    filename = "diplome/uploads/" + filename
    mon_image = Image.open(filename)
    message = stg.recuperer(mon_image, 80)
    print("Message : ", message)
    # enelever les étoiles
    message = message.replace("*", "")
    os.system("echo " + message + " > message.txt")

    # Decrypter le QRcode
    imageqrcode='diplome/diplomeCree/qr_code.png'
    signature = dQRC.detecteQRcode(imageqrcode)
    print("signature:", signature)
    # TODO : encode le message en binaire
    os.system("echo " + signature + " > signature.sign")


    # TODO : comparer  stegano et QRcode
    # openssl verify with certificat
    # TODO : PENSER A VERIFIER L'ENCODAGE 64
    if (os.system("openssl dgst -sha256 -verify gestionCerficat/public.pem -signature signature.sign message.txt") == 0):
        print("Signature OK")
    else:
        print("Signature KO")
    return