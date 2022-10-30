import os
# créer une AC avec une configuration bien choisie
# créer un certificat racine
os.system("openssl req -x509 -config root-ca-cert.cnf -newkey rsa:2048 -out ca.pem -keyout private/private.pem -days 1826")


