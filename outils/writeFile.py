import os

def verifWriteMessageOnFile(message, nomFichier):
    with open(nomFichier, 'r') as f:
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

def verifWriteMessageOnFileBinary(message, nomFichier):
    with open(nomFichier, 'rb') as f:
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

def writeMessageOnFileBinary(message, nomFichier):
    with open(nomFichier, 'wb') as f:
        f.write(message)
        # close the file
        f.close()
    verifWriteMessageOnFileBinary(message, nomFichier)
    return

def writeMessageOnFile(message, nomFichier):
    with open(nomFichier, 'w') as f:
        f.write(message)
        # close the file
        f.close()
    verifWriteMessageOnFile(message, nomFichier)
    return

def verifFichierExiste(nomFichier):
    if not os.path.isfile(nomFichier):
        print("Le fichier n'existe pas")
        exit(1)
        return False
    return True