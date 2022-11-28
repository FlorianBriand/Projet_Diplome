import os


def verifWriteMessageOnFile(message, nomFichier, mode):
    with open(nomFichier, mode) as f:
        messageVerif = f.read()
        # close the file
        f.close()
    if messageVerif != message:
        if not os.path.isfile(nomFichier):
            print("Le fichier n'existe pas")
            return False
        print("Erreur lors de l'écriture du message")
        exit(1)
    return


def writeMessageOnFile(message, nomFichier, mode):
    with open(nomFichier, mode) as f:
        f.write(message)
        # close the file
        f.close()
    # si mode = "w" ou "a" on read
    if mode == "w" or mode == "a":
        verifWriteMessageOnFile(message, nomFichier, 'r')
    else:
        verifWriteMessageOnFile(message, nomFichier, 'rb')
    return


def verifFichierExiste(nomFichier):
    if not os.path.isfile(nomFichier):
        print("Le fichier " + nomFichier + " n'existe pas")
        exit(1)
        return False
    return True
