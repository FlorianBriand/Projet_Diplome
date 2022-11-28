import os

CHEMIN_ACCES_OPENSSL = "C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe"

# créer une AC avec une configuration bien choisie
# créer un certificat racine
# PASS PHRASE : TOTO
os.system(
    CHEMIN_ACCES_OPENSSL + " req -x509 -config root-ca-cert.cnf -newkey rsa:2048 -out ca.pem -keyout private/private.pem -days 1826")
# C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe req -x509 -config root-ca-cert.cnf -newkey rsa:2048 -out ca.pem -keyout private/private.pem -days 1826

# extract public key from certificate
os.system(CHEMIN_ACCES_OPENSSL + " x509 -pubkey -noout -in ca.pem > public.pem")
# C:\\MesProgrammes\\OpenSSL-Win64\\bin\\openssl.exe x509 -pubkey -noout -in ca.pem > public.pem

# openssl sign
os.system("echo florian  > code.txt")
os.system(
    "openssl dgst -sha256 -passin pass:toto -sign gestionCertificat/private/private.pem -out sha256.sign code.txt")

# openssl verify with certificat
if (os.system(CHEMIN_ACCES_OPENSSL + " dgst -sha256 -verify public.pem -signature sha256.sign code.txt") == 0):
    print("Signature OK")
else:
    print("Signature KO")
