#!/usr/bin/python
# coding=utf8
import os

from PIL import Image


# fonction qui récupère le nom,prenom,diplome,timestamp du message
def recupInfo(message):
    nom = message.split("||")[0]
    prenom = message.split("||")[1]
    nomDiplome = message.split("||")[2]
    timestamp = message.split("||")[3]
    return nom, prenom, nomDiplome, timestamp


def recupImageStegano(filename):
    # localisation du fichier
    filename = "diplome/uploads/" + filename
    # message d'erreur si le fichier n'existe pas
    if not os.path.isfile(filename):
        print("Le fichier n'existe pas")
        return False
    mon_image = Image.open(filename)
    # message d'erreur si le fichier n'est pas une image
    if not mon_image:
        print("Le fichier n'est pas une image")
        return False
    return mon_image


def vers_8bit(c):
    chaine_binaire = bin(ord(c))[2:]
    return "0" * (8 - len(chaine_binaire)) + chaine_binaire


def modifier_pixel(pixel, bit):
    # on modifie que la composante rouge
    r_val = pixel[0]
    rep_binaire = bin(r_val)[2:]
    rep_bin_mod = rep_binaire[:-1] + bit
    r_val = int(rep_bin_mod, 2)
    return tuple([r_val] + list(pixel[1:]))


def recuperer_bit_pfaible(pixel):
    r_val = pixel[0]
    return bin(r_val)[-1]


def cacher(image, message):
    dimX, dimY = image.size
    im = image.load()
    message_binaire = ''.join([vers_8bit(c) for c in message])
    posx_pixel = 0
    posy_pixel = 0
    for bit in message_binaire:
        im[posx_pixel, posy_pixel] = modifier_pixel(im[posx_pixel, posy_pixel], bit)
        posx_pixel += 1
        if (posx_pixel == dimX):
            posx_pixel = 0
            posy_pixel += 1
        assert (posy_pixel < dimY)


def recuperer(image, taille):
    message = ""
    dimX, dimY = image.size
    im = image.load()
    posx_pixel = 0
    posy_pixel = 0
    for rang_car in range(0, taille):
        rep_binaire = ""
        for rang_bit in range(0, 8):
            rep_binaire += recuperer_bit_pfaible(im[posx_pixel, posy_pixel])
            posx_pixel += 1
            if (posx_pixel == dimX):
                posx_pixel = 0
                posy_pixel += 1
        message += chr(int(rep_binaire, 2))
    # close the file
    image.close()
    return message


'''
if __name__ == "__main__":


    mon_image = Image.open("diplome/diplomeCree/stegano_R_R.png")
    message_retrouve = recuperer(mon_image, 80)
    print(message_retrouve)


# Valeurs par defaut
nom_defaut = "image_test.png"
message_defaut = "Florian Briand CY Tech" + str(time.time())+"**********"
choix_defaut = 1

# programme de demonstration
saisie = input("Entrez l'operation 1) cacher 2) retrouver [%d]"%choix_defaut)
choix = saisie or choix_defaut

if choix == 1:
	saisie = input("Entrez le nom du fichier [%s]"%nom_defaut)
	nom_fichier = saisie or nom_defaut
	saisie = input("Entrez le message [%s]"%message_defaut)
	message_a_traiter = saisie or message_defaut
	print ("Longueur message : ",len(message_a_traiter))
	mon_image = Image.open(nom_fichier)
	cacher(mon_image, message_a_traiter)
	mon_image.save("stegano_"+nom_fichier)
else :
	saisie = input("Entrez le nom du fichier [%s]"%nom_defaut)
	nom_fichier = saisie or nom_defaut
	saisie = input("Entrez la taille du message ")
	message_a_traiter = int(saisie)
	mon_image = Image.open(nom_fichier)
	message_retrouve = recuperer(mon_image, message_a_traiter)
	print (message_retrouve)
'''
