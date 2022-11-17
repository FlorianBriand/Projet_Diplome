import os
import detecteQRcode as dQRC
import stegano as stg
from PIL import Image

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

def verifDiplome(filename):
    print("Vérification du diplome en cours...")
    #localisation du fichier
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


    print("Décryptage stégano en cours...")

    # Decrypter la stegano
    message = stg.recuperer(mon_image, 80)
    print("Message récupéré par stegano : ", message)
    # on récupère le nom et le prénom
    nom, prenom, nomDiplome, timestamp = recupInfo(message)
    # enlever les étoiles
    message = message.replace("*", "")
    os.system("echo " + message + " > stg_message.txt")

    # Decrypter le QRcode
    # TODO Changer le nom du fichier par le fichier uploadé
    imageqrcode="diplome/diplomeCree/"+nom+"_"+prenom+".png"
    # verifier que le fichier existe
    if not os.path.isfile(imageqrcode):
        print("Le fichier n'existe pas")
        return False

    signature = dQRC.detecteQRcode(imageqrcode)
    print("signature:", signature)
    # TODO : encode le message en binaire
    os.system("echo " + signature + " > signature.sign")


    # TODO : comparer  stegano et QRcode
    # openssl verify with certificat
    # TODO : PENSER A VERIFIER L'ENCODAGE 64
    if (os.system(CHEMIN_ACCES_OPENSSL + " dgst -sha256 -verify gestionCerficat/public.pem -signature signature.sign stg_message.txt") == 0):
        print("Signature OK")
    else:
        print("Signature KO")
    return

# fonction qui récupère le nom,prenom,diplome,timestamp du message
def recupInfo(message):
    nom = message.split(" ")[0]
    prenom = message.split(" ")[1]
    nomDiplome = message.split(" ")[2]
    timestamp = message.split(" ")[3]
    return nom, prenom, nomDiplome, timestamp