import os

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