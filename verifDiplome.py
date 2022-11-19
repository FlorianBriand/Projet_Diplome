import os
from binascii import unhexlify
from outils import stegano as stg
from outils.stegano import recupImageStegano, recupInfo
from outils.writeFile import writeMessageOnFile, verifFichierExiste, writeMessageOnFileBinary
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

    writeMessageOnFile(message, TMP_STG_MESSAGE)
    return message


def saveSignatureQRcodeToTmpSign(message):

    nom, prenom, nomDiplome, timestamp = recupInfo(message)

    # TODO Changer le nom du fichier par le fichier uploadé
    imageqrcode = "diplome/diplomeCree/" + nom + "_" + prenom + ".png"

    verifFichierExiste(imageqrcode)

    signature = dQRC.detecteQRcode(imageqrcode)

    # encoder la signature en base2
    signature = unhexlify(signature)

    # écrire la signature dans un fichier
    writeMessageOnFileBinary(signature, TMP_SIGNATURE)


def verifSignature():
    verifFichierExiste(TMP_SIGNATURE)
    # TODO : comparer  stegano et QRcode
    # openssl verify with certificat
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
    saveSignatureQRcodeToTmpSign(message)
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
