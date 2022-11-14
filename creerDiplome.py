import os
from PIL import Image
import stegano as stg
import createQRcode as crQRC

def creerDiplome(nom, prenom, nomDiplome, timestamp):
    message = nom + " " + prenom + " " + nomDiplome + " " + timestamp
    # Mettre les informations en stégano dans l'image
    infoStegano(message, nom, prenom)
    # Signer les informations en stégano dans l'image avec la clé privée
    signatureMessage(message, nom, prenom)
    # Mettre la signature dans le QRcode
    crQRC.creerQRcode(nom, prenom)
    # TODO : Mettre le QRcode dans l'image

    return

def signatureMessage(message,nom,prenom):
    os.system("echo  " + message + " > code.txt")
    #os.system("openssl dgst -sha256 -sign private/private.pem -out sha256.sign code.txt")
    os.system("openssl dgst -sha256 -sign private/private.pem -out "+nom+"_"+prenom+".sign code.txt")
    # supprimer le fichier code.txt
    os.system("rm code.txt")
    return

def infoStegano(message, nom, prenom):
    imageCertif = Image.open("diplome/image_test.png")
    stg.cacher(imageCertif, message)
    imageCertif.save("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")
    return
