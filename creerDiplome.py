import os
from PIL import Image

from mail import envoiMailSecurise
from outils import stegano as stg
from outils.writeFile import writeMessageOnFile, verifFichierExiste
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

    # Insérer le QRcode dans l'image
    print("Etape 4 : Insérer le QRcode + Text dans l'image")
    insertQRcodeInImage(nom, prenom)
    insertTextInImage(nom, prenom)
    print("fini")

    print("Diplome créé avec succès")

    # Envoi du diplome par mail
    print("Etape 5 : Envoi du diplome par mail")
    print("en cours...")
    envoiMailSecurise(nom, prenom, email)
    print("fini")

    # Nettoyage des fichiers temporaires
    os.remove("diplome/diplomeCree/" + nom + "_" + prenom + ".png")
    os.remove("tmp_" + nom + "_" + prenom + ".txt")
    os.remove("diplome/diplomeCree/tmp_" + nom + "_" + prenom + ".sign")
    #os.remove("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    return


def insertQRcodeInImage(nom, prenom):
    verifFichierExiste("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")
    verifFichierExiste("diplome/diplomeCree/" + nom + "_" + prenom + ".png")

    # Opening the primary image
    img1 = Image.open("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    # Opening the secondary image (used as a watermark)
    img2 = Image.open(r"diplome/diplomeCree/" + nom + "_" + prenom + ".png")

    # Pasting img2 image on top of img1
    img1.paste(img2, (1400, 910))

    # Saving the image
    img1.save("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    # Closing the image
    img1.close()
    return


def insertTextInImage(nom, prenom):
    verifFichierExiste("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    # Opening the image
    img1 = Image.open("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    fonttitre = ImageFont.truetype("arial.ttf", 70)
    font = ImageFont.truetype("arial.ttf", 50)

    draw = ImageDraw.Draw(img1)

    draw.text((750, 350), "Diplôme", (0, 0, 0), font=fonttitre)
    draw.text((350, 500), prenom, (0, 0, 0), font=font)
    draw.text((350, 600), nom, (0, 0, 0), font=font)
    draw.text((350, 700), "CY Tech", (0, 0, 0), font=font)

    # save the image
    img1.save("diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png")

    # Closing the image
    img1.close()
    return


def signatureMessage(message, nom, prenom):
    nomfichier = "tmp_" + nom + "_" + prenom + ".txt"

    writeMessageOnFile(message, nomfichier, "w")

    commande = CHEMIN_ACCES_OPENSSL + " dgst -sha256 -passin pass:toto -sign gestionCertificat/private/private.pem -out " + EMPLACEMENT_DIPLOME_CREE + "tmp_" + nom + "_" + prenom + ".sign " + nomfichier
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
