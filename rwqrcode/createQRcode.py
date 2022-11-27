import os
from binascii import hexlify

import qrcode
from PIL import Image


def creerQRcode(nom, prenom):
    # Get the content of the .sign
    # and convert it to a string
    with open("diplome/diplomeCree/tmp_" + nom + "_" + prenom + ".sign", "rb") as f:
        content = f.read()
        f.close()
        content = hexlify(content)

        qrObject = qrcode.QRCode()
        qrObject.add_data(content)
        qrObject.make()
        img = qrObject.make_image()
        img.save("diplome/diplomeCree/" + nom + "_" + prenom + ".png")
        img.close()

        # Resize the qr code
        qrResize = Image.open("diplome/diplomeCree/" + nom + "_" + prenom + ".png")
        qrResize = qrResize.resize((250, 250))
        qrResize.save("diplome/diplomeCree/" + nom + "_" + prenom + ".png")
        qrResize.close()

        # Vérifier que le fichier a bien été créé
        if not os.path.isfile("diplome/diplomeCree/" + nom + "_" + prenom + ".png"):
            print("Le fichier n'a pas été créé")
            exit()

        return
