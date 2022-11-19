import os
from binascii import unhexlify

from PIL import Image
from outils.writeFile import writeMessageOnFile
from rwqrcode import detecteQRcode as dQRC
from outils import stegano as stg

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

def verifDiplome(filename):
    print("Vérification du diplome en cours...")
    # Récupération image
    image_stegano = recupImageStegano(filename)
    print("Décryptage stégano en cours...")
    # Decrypter la stegano
    message = stg.recuperer(image_stegano, 80)
    # on récupère le nom et le prénom
    nom, prenom, nomDiplome, timestamp = recupInfo(message)
    # enlever les étoiles
    message = message.replace("*", "")
    print("Message récupéré par stegano :" + message)
    nomfichier = "stg_message.txt"
    writeMessageOnFile(message, nomfichier)

    # Decrypter le QRcode
    # TODO Changer le nom du fichier par le fichier uploadé
    imageqrcode="diplome/diplomeCree/"+nom+"_"+prenom+".png"
    # verifier que le fichier existe
    if not os.path.isfile(imageqrcode):
        print("Le fichier n'existe pas")
        return False

    signature = dQRC.detecteQRcode(imageqrcode)

    print(signature)
    # encoder la signature en base2
    signature = unhexlify(signature)
    print("signature:", signature)
    os.system("echo "" > signature.sign ")
    file = open("signature.sign", "wb")
    file.write(signature)
    file.close()


    # verifier si le fichier existe
    if not os.path.isfile("signature.sign"):
        print("Le fichier n'existe pas")
        return False

    # TODO : comparer  stegano et QRcode
    # openssl verify with certificat
    if (os.system(CHEMIN_ACCES_OPENSSL + " dgst -sha256 -verify gestionCertificat/public.pem -signature signature.sign stg_message.txt") == 0):
        print("Signature OK")
    else:
        print("Signature KO")

# fonction qui récupère le nom,prenom,diplome,timestamp du message
def recupInfo(message):
    nom = message.split("||")[0]
    prenom = message.split("||")[1]
    nomDiplome = message.split("||")[2]
    timestamp = message.split("||")[3]
    return nom, prenom, nomDiplome, timestamp

def recupImageStegano(filename):
    # localisation du fichier
    filename = "diplome/uploads/" + filename
    # message d'erreur si le fichier n'existe pas
    if not os.path.isfile(filename):
        print("Le fichier n'existe pas")
        return False
    mon_image = Image.open(filename)
    # message d'erreur si le fichier n'est pas une image
    if not mon_image:
        print("Le fichier n'est pas une image")
        return False
    return mon_image