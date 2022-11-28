import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart

from outils.writeFile import verifFichierExiste

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"
MAIL_FROM = "projetcryptofloraph@gmail.com"
MAIL_TO = ""
STEGANO_FILE = ""
COMMANDE_AFFICHE = "type"
CERTIFICAT = "gestionCertificat/ca.pem"
TMP_CONTENU_MAIL = "contenu.txt"
TMP_CONTENU_COURRIER = "contenu_courrier.txt"


def affichageErreurSignatureMail(resultatEnvoieMail):
    if (resultatEnvoieMail == 0):
        print("Création du contenu sécurisé réussi")
    elif (resultatEnvoieMail == 1):
        print("an error occurred parsing the command options.")
    elif (resultatEnvoieMail == 2):
        print("an error occurred reading the input file.")
    elif (resultatEnvoieMail == 3):
        print("an error occurred creating the PKCS#7 file or when reading the MIME message.")
    elif (resultatEnvoieMail == 4):
        print("an error occurred decrypting or verifying the message.")
    else:
        print("the message was verified correctly but an error occurred writing out the signers certificates.")


def envoiMail(msg):
    verifFichierExiste(TMP_CONTENU_COURRIER)
    with open(TMP_CONTENU_COURRIER, "r") as contenu_courrier:
        mail = contenu_courrier.read()
        contenu_courrier.close()
    mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mailserver.login(msg['From'], 'jrvzgmrmtsotmzct')
    # Verifie si le mail est envoyé
    resultatEnvoieMail = mailserver.sendmail(msg['From'], msg['To'], mail)
    if resultatEnvoieMail != {}:
        print("Erreur lors de l'envoie du mail")
    else:
        print("Mail envoyé avec succès")

    mailserver.quit()


def lectureContenuMail():
    verifFichierExiste(STEGANO_FILE)
    with open(STEGANO_FILE, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

    with open(TMP_CONTENU_MAIL, "w") as contenu:
        messageContenu = str(encoded_string)
        # Enlever les caractères b' et ' de la chaine de caractère
        messageContenu = messageContenu[2:-1]

        # header du mail avec png en pièce jointe
        contenu.write("Content-Type: image/png; name=\"diplome_" + MAIL_TO + ".png\"\r")
        contenu.write("Content-Transfer-Encoding: base64\r")
        contenu.write(messageContenu)
        # fermeture du fichier
        contenu.close()


def envoiMailSecurise(nom, prenom, email):
    global MAIL_TO
    MAIL_TO = email
    global STEGANO_FILE
    STEGANO_FILE = "diplome/diplomeCree/stegano_" + nom + "_" + prenom + ".png"

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM
    msg['To'] = MAIL_TO

    lectureContenuMail()

    commande = CHEMIN_ACCES_OPENSSL + \
               " smime -sign -in " + TMP_CONTENU_MAIL + " -out " + TMP_CONTENU_COURRIER + " -signer " + \
               CERTIFICAT + " -inkey gestionCertificat/private/private.pem" \
                            " -passin pass:toto -from '" + MAIL_FROM + "' -to '" + MAIL_TO + "' -subject 'Envoicertificat'"

    resultatEnvoieMail = os.system(commande)

    affichageErreurSignatureMail(resultatEnvoieMail)

    envoiMail(msg)

    # Nettoyage des fichiers
    os.remove(TMP_CONTENU_MAIL)
    os.remove(TMP_CONTENU_COURRIER)


if __name__ == '__main__':
    envoiMailSecurise()
