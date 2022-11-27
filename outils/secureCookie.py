import random

from outils.writeFile import verifFichierExiste

EMPLACEMENT_FICHIER_COOKIE = "outils/tokenSession.txt"


def verifCookie(cookie):
    # initialise la liste des cookies avec le fichier tokenSession.txt
    listeCookie = []
    verifFichierExiste(EMPLACEMENT_FICHIER_COOKIE)
    with open(EMPLACEMENT_FICHIER_COOKIE, 'r') as f:
        for line in f:
            listeCookie.append(line)
        f.close()

    # si le cookie se trouve dans la liste des cookies valides alors on renvoie 0
    if cookie in listeCookie:
        return True
    # sinon on renvoie 1
    else:
        return False


# Génère un mot de passe aléatoire de 8 caractères 0-9, a-z, A-Z

def generatePasswordWriteItInFile():
    password = ""
    for i in range(14):
        password += chr(random.randint(33, 126))
    verifFichierExiste(EMPLACEMENT_FICHIER_COOKIE)
    with open(EMPLACEMENT_FICHIER_COOKIE, 'a') as f:
        f.write(password + '\n')
        f.close()
    return password
