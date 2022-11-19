from binascii import hexlify

import qrcode

def creerQRcode(nom, prenom):
    # Get the content of the .sign
    # and convert it to a string
    with open("diplome/diplomeCree/tmp_"+nom+"_"+prenom+".sign", "rb") as f:

        content = f.read()
        print("AVant encodage" + str(content))
        content = hexlify(content)
        print(content)

        # Create qr code instance with the file sha256.sign
        qr = qrcode.make(content)
        # Save the qr code as a png file
        qr.save("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        return