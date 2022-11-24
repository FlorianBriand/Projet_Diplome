import os
from PIL import Image

from mail import envoiMailSecurise
from outils import stegano as stg
from outils.writeFile import writeMessageOnFile
from rwqrcode import createQRcode as crQRC

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"
EMPLACEMENT_DIPLOME_CREE = "diplome/diplomeCree/"

def creerDiplome(nom, prenom, nomDiplome, timestamp, email):
    # Notre message
    message = nom + "||" + prenom + "||" + nomDiplome + "||" + timestamp

    # Lancement de la création du diplome
    print("Création du diplome en cours...")

    # Mettre les informations en stégano dans l'image
    print("Etape 1 : Création de l'image stégano")

    print("en cours...")
    creerPNGDiplomeStegano(message, nom, prenom)
    print("fini")

    # Signer les informations en stégano dans l'image avec la clé privée
    print("Etape 2 : Signature du message")

    print("en cours...")
    signatureMessage(message, nom, prenom)
    print("fini")

    # Mettre la signature dans le QRcode
    print("Etape 3 : Création du QRcode")

    print("en cours...")
    crQRC.creerQRcode(nom, prenom)
    print("fini")

    # TODO : DELETE the nom_prenom.sign
    # TODO : Mettre le QRcode dans l'image

    print("Diplome créé avec succès")

    # Envoi du diplome par mail
    print("Etape 4 : Envoi du diplome par mail")
    print("en cours...")
    envoiMailSecurise(nom, prenom, email)
    print("fini")

    # Nettoyage des fichiers temporaires
    os.remove("tmp_" + nom + "_" + prenom + ".txt")
    os.remove("diplome/diplomeCree/tmp_"+nom+"_"+prenom+".sign")
    os.remove("diplome/diplomeCree/stegano_"+nom+"_"+prenom+".png")

    return

def signatureMessage(message,nom,prenom):
    nomfichier = "tmp_" + nom + "_" + prenom + ".txt"

    writeMessageOnFile(message, nomfichier, "w")

    commande = CHEMIN_ACCES_OPENSSL + " dgst -sha256 -passin pass:toto -sign gestionCertificat/private/private.pem -out " +EMPLACEMENT_DIPLOME_CREE+"tmp_" + nom +"_" + prenom +".sign " + nomfichier
    resultatSignature = os.system(commande)

    if (resultatSignature == 0):
        print("Signature réussie")
    else:
        print("Erreur lors de la signature")
    return

def creerPNGDiplomeStegano(message, nom, prenom):
    # Vérifier si le fichier existe
    if not os.path.isfile("diplome/image_test.png"):
        print("Le fichier template n'existe pas")
        return False

    imageCertif = Image.open("diplome/image_test.png")
    # Completer le message avec des étoiles pour avoir une taille de 80 caractères
    message = message + "*" * (80 - len(message))
    stg.cacher(imageCertif, message)

    imageCertif.save(EMPLACEMENT_DIPLOME_CREE + "stegano_" + nom + "_" + prenom + ".png")
    # close the file
    imageCertif.close()
    return
