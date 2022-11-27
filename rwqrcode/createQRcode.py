import os
from binascii import hexlify
from PIL import Image

import qrcode
from qrcode import ERROR_CORRECT_L

from pyzbar.pyzbar import decode


def creerQRcode(nom, prenom):
    # Get the content of the .sign
    # and convert it to a string
    with open("diplome/diplomeCree/tmp_"+nom+"_"+prenom+".sign", "rb") as f:

        content = f.read()
        f.close()
        content = hexlify(content)


        qrObject = qrcode.QRCode()
        qrObject.add_data(content)
        qrObject.make()
        img = qrObject.make_image()
        img.save("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        img.close()

        # Resize the qr code
        qrResize = Image.open("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        qrResize = qrResize.resize((250, 250))
        qrResize.save("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        qrResize.close()

        # Vérifier que le fichier a bien été créé
        if not os.path.isfile("diplome/diplomeCree/"+nom+"_"+prenom+".png"):
            print("Le fichier n'a pas été créé")
            exit()

        return

# TODO A supprimer
if __name__ == '__main__':


    content = "https://www.youtube.com/468468468468fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff4648646666666666666666666666666666666666666666666hiuhiuhiuhiuhiuhiuhiuhihiuuh66666666hiuhiuhiuhihiuhiu66646464646o"
    content = content + content + content + content + content + content
    print(len(content))

    qrObject = qrcode.QRCode(version=1, error_correction=ERROR_CORRECT_L, box_size=5)
    qrObject.add_data(content)
    qrObject.make()
    img = qrObject.make_image()

    # Save the qr code as a png file
    img.save("../diplome/diplomeCree/Briand_Florian.png")

    qrResize = Image.open("../diplome/diplomeCree/Briand_Florian.png")
    qrResize = qrResize.resize((250, 250))
    qrResize.save("../diplome/diplomeCree/Briand_Florian.png")
    qrResize.close()


    decodeQR=decode(Image.open("../diplome/diplomeCree/stegano_Briand_Florian.png"))
    if decodeQR==[]:
        print("Résultat de vérification de la signature cachée par QR : False")
    else :
        print("Résultat de vérification de la signature cachée par QR : True")
        res =decodeQR[0].data.decode("utf-8")
        print(res)


        print(decodeQR)

