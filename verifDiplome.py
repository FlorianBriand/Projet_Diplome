import os
from binascii import unhexlify

from outils import stegano as stg
from outils.stegano import recupImageStegano, recupInfo
from outils.writeFile import writeMessageOnFile, verifFichierExiste
from rwqrcode import detecteQRcode as dQRC

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"
EMPLACEMENT_CLE_PUBLIQUE = "gestionCertificat/public.pem"
TMP_SIGNATURE = "tmp_signature.sign"
TMP_STG_MESSAGE = "stg_message.txt"


def saveMessageSteganoToTmpTxt(filename):
    image_stegano = recupImageStegano(filename)
    message = stg.recuperer(image_stegano, 80)
    # enlever les étoiles
    message = message.replace("*", "")

    writeMessageOnFile(message, TMP_STG_MESSAGE, "w")
    return message


def saveSignatureQRcodeToTmpSign(message, filename):
    nom, prenom, nomDiplome, timestamp = recupInfo(message)

    imageqrcode = "diplome/uploads/" + filename

    verifFichierExiste(imageqrcode)

    signature = dQRC.detecteQRcode(imageqrcode)

    # encoder la signature en base2
    signature = unhexlify(signature)

    # écrire la signature dans un fichier
    writeMessageOnFile(signature, TMP_SIGNATURE, "wb")


def verifSignature():
    verifFichierExiste(TMP_SIGNATURE)
    verifFichierExiste(TMP_STG_MESSAGE)
    verifFichierExiste(EMPLACEMENT_CLE_PUBLIQUE)

    commande = CHEMIN_ACCES_OPENSSL + " dgst -sha256 -verify " + EMPLACEMENT_CLE_PUBLIQUE + " -signature " + TMP_SIGNATURE + " " + TMP_STG_MESSAGE

    return os.system(commande)


def verifDiplome(filename):
    print("Vérification du diplome en cours...")

    print("Etape 1 : Décryptage stégano")
    print("en cours...")
    message = saveMessageSteganoToTmpTxt(filename)
    print("fini")

    print("Etape 2 : Lecture du QRcode")
    print("en cours...")
    saveSignatureQRcodeToTmpSign(message, filename)
    print("fini")

    print("Etape 3 : Vérification de la signature")
    print("en cours...")
    resultatSignature = verifSignature()
    print("fini")

    # Nettoyage des fichiers temporaires
    os.remove(TMP_SIGNATURE)
    os.remove("diplome/uploads/" + filename)
    os.remove(TMP_STG_MESSAGE)

    if resultatSignature == 0:
        print("Le diplome est valide")
    else:
        print("Le diplome est invalide")
    return resultatSignature
