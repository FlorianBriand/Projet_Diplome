import os
from PIL import Image
import stegano as stg
import createQRcode as crQRC


CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

def creerDiplome(nom, prenom, nomDiplome, timestamp):
    # Lancement de la création du diplome
    print("Création du diplome en cours...")
    message = nom + "||" + prenom + "||" + nomDiplome + "||" + timestamp
    # Mettre les informations en stégano dans l'image
    creerPNGDiplomeStegano(message, nom, prenom)
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
    nomFichier = "code.txt"
    writeMessageOnFile(message,nomFichier)

    resultatSignature = os.system(CHEMIN_ACCES_OPENSSL + " dgst -sha256 -passin pass:toto -sign gestionCertificat/private/private.pem -out diplome/diplomeCree/"+nom+"_"+prenom+".sign code.txt")
    if (resultatSignature == 0):
        print("Signature OK")
    else:
        print("Erreur lors de la signature")
        exit(1)
    # supprimer le fichier code.txt
    os.system("del code.txt")
    return

def creerPNGDiplomeStegano(message, nom, prenom):
    imageCertif = Image.open("diplome/image_test.png")
    # Completer le message avec des étoiles pour avoir une taille de 80 caractères
    message = message + "*" * (80 - len(message))
    print("message : ", message)
    stg.cacher(imageCertif, message)
    imageCertif.save("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")
    return


def verifWriteMessageOnFile(message, nomFichier):
    with open(nomFichier, 'r') as f:
        messageVerif = f.read()
        # close the file
        f.close()
    if messageVerif == message:
        print("Ecriture OK")
    else:
        if not os.path.isfile(nomFichier):
            print("Le fichier n'existe pas")
            return False
        print("Erreur lors de l'écriture du message")
        exit(1)
    return

def writeMessageOnFile(message, nomFichier):
    with open(nomFichier, 'w') as f:
        f.write(message)
        # close the file
        f.close()

    verifWriteMessageOnFile(message, nomFichier)
    return

