import os
from binascii import hexlify

import qrcode

def creerQRcode(nom, prenom):
    # Get the content of the .sign
    # and convert it to a string
    with open("diplome/diplomeCree/tmp_"+nom+"_"+prenom+".sign", "rb") as f:

        content = f.read()
        f.close()
        print("AVant encodage" + str(content))
        content = hexlify(content)
        print(content)

        # Create qr code instance with the file sha256.sign
        qr = qrcode.make(content)
        # Save the qr code as a png file
        qr.save("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        # Vérifier que le fichier a bien été créé
        if not os.path.isfile("diplome/diplomeCree/"+nom+"_"+prenom+".png"):
            print("Le fichier n'a pas été créé")
            exit()

        return