#!/usr/bin/python
# coding=utf8
import base64
import os
import struct
import hashlib
import time
from PIL import Image

def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

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

def cacher(image,message):
	dimX,dimY = image.size
	im = image.load()
	message_binaire = ''.join([vers_8bit(c) for c in message])
	posx_pixel = 0
	posy_pixel = 0
	for bit in message_binaire:
		im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
		posx_pixel += 1
		if (posx_pixel == dimX):
			posx_pixel = 0
			posy_pixel += 1
		assert(posy_pixel < dimY)

def recuperer(image,taille):
	message = ""
	dimX,dimY = image.size
	im = image.load()
	posx_pixel = 0
	posy_pixel = 0
	for rang_car in range(0,taille):
		rep_binaire = ""
		for rang_bit in range(0,8):
			rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
			posx_pixel +=1
			if (posx_pixel == dimX):
				posx_pixel = 0
				posy_pixel += 1
		message += chr(int(rep_binaire, 2))
	return message

def GoogleAuthenticatorCode(secret):
	key = base64.b32decode(secret)
	msg = struct.pack(">Q", int(time.time()) // 30)
	h = hashlib.new("sha1", key + msg).digest()
	o = h[19] & 15
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
	return str(h).zfill(6)

print ("Début du programme")
secret = "FBSWY3DPEHPK3PXP"
print ("Secret : " + secret)
code = GoogleAuthenticatorCode(secret)
print ("Code : " + code)




# Ne marche pas
#os.system("openssl dgst -sha256 -sign private.pem -out sha1.sign "florianbriand")
#os.system("openssl dgst -sha256 -verify ca.pem -signature sha1.sign test.txt")


'''

# Valeurs par defaut
nom_defaut = "image_test.png"
message_defaut = "Florian Briand CY Tech" + str(time.time())
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

