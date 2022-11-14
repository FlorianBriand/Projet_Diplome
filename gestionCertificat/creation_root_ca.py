import os
# créer une AC avec une configuration bien choisie
# créer un certificat racine
# PASS PHRASE : TOTO
os.system("openssl req -x509 -config root-ca-cert.cnf -newkey rsa:2048 -out ca.pem -keyout private/private.pem -days 1826")

# openssl sign string
os.system("echo florian  > code.txt")
os.system("openssl dgst -sha256 -sign private/private.pem -out sha256.sign code.txt")
# extract public key from certificate
os.system("openssl x509 -pubkey -noout -in ca.pem > public.pem")
# openssl verify with certificat
os.system("openssl dgst -sha256 -verify public.pem -signature sha256.sign code.txt")
if (os.system("openssl dgst -sha256 -verify public.pem -signature sha256.sign code.txt") == 0):
    print("Signature OK")
else:
    print("Signature KO")


