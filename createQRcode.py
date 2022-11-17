import base64

import qrcode

def creerQRcode(nom, prenom):
    # Get the content of the .sign
    # and convert it to a string
    # TODO : A changer par le nom et le prenom de la personne
    #with open("gestionCertificat/"+nom+"_"+prenom+".sign", "rb") as f:
    with open("gestionCertificat/sha256.sign", "rb") as f:
        content = f.read()
        # decode the content to base 64
        content = base64.b64encode(content)
        print(content)

        # Create qr code instance with the file sha256.sign
        qr = qrcode.make(content)
        # Save the qr code as a png file
        qr.save("diplome/diplomeCree/"+nom+"_"+prenom+".png")
        return