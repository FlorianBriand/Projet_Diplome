import os
from PIL import Image
import stegano as stg
import createQRcode as crQRC

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

def creerDiplome(nom, prenom, nomDiplome, timestamp):
    # Lancement de la création du diplome
    print("Création du diplome en cours...")
    message = nom + " " + prenom + " " + nomDiplome + " " + timestamp
    # Mettre les informations en stégano dans l'image
    infoStegano(message, nom, prenom)
    print("Stegano OK : ", message)
    # Signer les informations en stégano dans l'image avec la clé privée
    print("Signature en cours...")
    signatureMessage(message, nom, prenom)

    # Mettre la signature dans le QRcode
    crQRC.creerQRcode(nom, prenom)
    # TODO : DELETE the nom_prenom.sign
    # TODO : Mettre le QRcode dans l'image

    return

def signatureMessage(message,nom,prenom):
    os.system("echo  " + message + " > code.txt")
    resultatSignature = os.system(CHEMIN_ACCES_OPENSSL + " dgst -sha256 -passin pass:toto -sign gestionCertificat/private/private.pem -out diplome/diplomeCree/"+nom+"_"+prenom+".sign code.txt")
    print("resultatSignature : ", resultatSignature)
    if (resultatSignature == 0):
        print("Signature OK")
    else:
        print("Erreur lors de la signature")
        exit(1)
    # supprimer le fichier code.txt
    os.system("del code.txt")
    return

def infoStegano(message, nom, prenom):
    imageCertif = Image.open("diplome/image_test.png")
    # Completer le message avec des étoiles pour avoir une taille de 80 caractères
    message = message + "*" * (80 - len(message))
    print("message : ", message)
    stg.cacher(imageCertif, message)
    imageCertif.save("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")
    return
