import os
from PIL import Image
import stegano as stg
from rwqrcode import createQRcode as crQRC

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

def creerDiplome(nom, prenom, nomDiplome, timestamp):
    # Notre message
    message = nom + "||" + prenom + "||" + nomDiplome + "||" + timestamp

    # Lancement de la création du diplome
    print("Création du diplome en cours...")

    # Mettre les informations en stégano dans l'image
    print(" Etape 1 : Création de l'image stégano")

    print("en cours...")
    creerPNGDiplomeStegano(message, nom, prenom)
    print("fini")

    # Signer les informations en stégano dans l'image avec la clé privée
    print(" Etape 2 : Signature du message")

    print("en cours...")
    signatureMessage(message, nom, prenom)
    print("fini")

    # Mettre la signature dans le QRcode
    print(" Etape 3 : Création du QRcode")

    print("en cours...")
    crQRC.creerQRcode(nom, prenom)
    print("fini")

    # TODO : DELETE the nom_prenom.sign
    # TODO : Mettre le QRcode dans l'image

    print("Diplome créé avec succès")

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
    #os.system("del code.txt")
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

