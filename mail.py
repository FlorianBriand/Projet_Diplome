import base64
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"
MAIL_FROM = "projetcryptofloraph@gmail.com"
MAIL_TO = "briandflor@cy-tech.fr"
STEGANO_FILE = "diplome/diplomeCree/stegano_S_S.png"
COMMANDE_AFFICHE = "type"
CERTIFICAT = "gestionCertificat/ca.pem"


def envoiMail():
    # encode image to base64

    # Création du message
    msg = MIMEMultipart()
    msg['From'] = 'projetcryptofloraph@gmail.com'
    msg['To'] = 'coutinhora@cy-tech.fr'

    with open(STEGANO_FILE, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        image_file.close()

    with open("contenu.txt", "w") as contenu:
        contenu.write("Content-Type: image/png\r\nContent-Transfer-Encoding: base64\r\n\r\n" + str(encoded_string))
        # fermeture du fichier
        contenu.close()
        
        commande = COMMANDE_AFFICHE+" contenu.txt | " + CHEMIN_ACCES_OPENSSL + " smime -passin pass:toto -signer "+ CERTIFICAT +" -from '" + MAIL_FROM + "' -to '" + MAIL_TO + "' -subject 'Envoi certificat' -sign -inkey gestionCertificat/private/private.pem -out contenu_courrier.txt"
        print(commande)
        os.system(commande)

    with open("contenu_courrier.txt", "r") as contenu_courrier:
        mail = contenu_courrier.read()
    contenu_courrier.close()

    # Envoi du mail
    mailserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    mailserver.login(msg['From'], 'jrvzgmrmtsotmzct')
    mailserver.sendmail(MAIL_FROM, MAIL_TO, mail)
    mailserver.quit()

    # os.system("cat contenu.txt")


if __name__ == '__main__':
    # envoyer un mail automatiquement
    envoiMail()
    print('Mail envoyé')
