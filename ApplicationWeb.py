from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, make_response

import creerDiplome as cd
import verifDiplome as vd
from outils.GoogleAuthentificator import GoogleAuthenticatorCode
from outils.secureCookie import generatePasswordWriteItInFile, verifCookie

EMPLACEMENT_DIPLOMES = "diplome/diplomeCree/diplomes.txt"

app = Flask(__name__)

# TODO Créer le readme
@app.route("/")
def hello_world():
    return """
    <html>
    <head>
    <title>Diplome</title>
    </head>
    <body>
    <h1>Diplôme digital</h1>
    <a href="/creerDiplome">Créer un diplôme</a>
    <br>
    <a href="/verifDiplome">Vérifier un diplôme</a>
    <br>
    <a href="/listeDiplomes">Liste des diplômes</a>
    </body>
    </html>
    """


@app.route('/creerDiplome', methods=['GET', 'POST'])
def creerDiplome():
    # Vérification si l'utilisateur possède le cookie ou qu'il n'est pas égale à 0
    if request.cookies.get('otp') == None or verifCookie(request.cookies.get('otp')):
        # Redirection vers la page de vérification OTP
        return redirect(url_for('verifOTP'))

    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        if request.form['nom'] and request.form['prenom'] and request.form['nomDiplome'] and request.form['email']:
            nom = request.form['nom']
            prenom = request.form['prenom']
            nomDiplome = request.form['nomDiplome']
            email = request.form['email']
            # get timestamp
            # TODO Certifier le timestamp
            now = datetime.now()
            timestamp = str(round(datetime.timestamp(now)))
            print("timestamp =", timestamp)
        # sinon on renvoie une erreur
        else:
            return "Erreur, veuillez remplir tous les champs"

        cd.creerDiplome(nom, prenom, nomDiplome, timestamp, email)

        # Insérer les valeurs dans un fichier texte
        newligne = nom + '||' + prenom + '||' + nomDiplome + '||' + timestamp + '||' + email + '\n'
        with open(EMPLACEMENT_DIPLOMES, 'a') as f:
            f.write(newligne)
            f.close()

        # Rediriiger vers la liste des diplomes
        return "Le diplôme a bien été créé" \
               "<br>" \
               "<a href='/'>Retour à l'accueil</a>" \
               "<br>" \
               "<a href='/listeDiplomes'>Voir la liste des diplômes</a>"
    else:
        return render_template('creerDiplome.html')


@app.route('/listeDiplomes')
def listeDiplomes():
    # Lire le fichier texte et stocker dans une liste de diplomes
    diplomes = []
    with open('diplome/diplomeCree/diplomes.txt', 'r') as f:
        for line in f:
            nom, prenom, nomDiplome, timestamp, email = line.split('||')
            diplomes.append(
                {'nom': nom, 'prenom': prenom, 'nomDiplome': nomDiplome, 'timestamp': timestamp, 'email': email})
        # close the file
        f.close()
    return render_template('listeDiplomes.html', diplomes=diplomes)


# Verfier le fichier uploadé
@app.route('/verifDiplome', methods=['GET', 'POST'])
def verifDiplom():
    if request.method == 'POST':
        # Récupérer le fichier uploadé
        f = request.files['file']
        # Sauvegarder le fichier dans le dossier upload
        f.save('diplome/uploads/' + f.filename)
        resultatVerifSignature = vd.verifDiplome(f.filename)
        if resultatVerifSignature == 0:
            return "Le diplôme est valide" \
                   "<br>" \
                   "<a href='/'>Retour</a>" \
                   "<br>" \
                   "<a href='/verifDiplome'>Vérifier un autre diplôme</a>"
        else:
            return "Le diplôme est invalide" \
                   "<br>" \
                   "<a href='/'>Retour</a>" \
                   "<br>" \
                   "<a href='/verifDiplome'>Vérifier un autre diplôme</a>"

    else:
        return render_template('verifDiplome.html')


# OTP
@app.route('/verifOTP', methods=['GET', 'POST'])
def verifOTP():
    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        if request.form['otp']:
            otp = request.form['otp']
            if otp == GoogleAuthenticatorCode("FBSWY3DPEHPK3PXP"):
                # Créer le cookie
                resp = make_response(render_template('creerDiplome.html'))

                # Valeur aléatoire comprise entre 0-9 a-z A-Z
                cookieValue = generatePasswordWriteItInFile()

                resp.set_cookie('otp', cookieValue)
                return resp
            else:
                return "Erreur, OTP incorrect" \
                       "<br>" \
                       "<a href='/'>Retour</a>" \
                    # sinon on renvoie une erreur
        else:
            return "Erreur, veuillez remplir tous les champs"
    else:
        return render_template('otp.html')


@app.route('/regenDiplome', methods=['GET', 'POST'])
def regenDiplome():
    # Récuper la valeur en paramètre
    timestamp = request.args.get('time')
    nom = request.args.get('nom')
    prenom = request.args.get('prenom')
    nomDiplome = request.args.get('nomDiplome')
    email = request.args.get('email')

    # si le timestamp ou le nom ou le prenom ou le nomDiplome ou l'email est vide
    if timestamp == None or nom == None or prenom == None or nomDiplome == None or email == None:
        return "Erreur, dans les paramètres de l'url" \
               "<br>" \
               "<a href='/listeDiplomes'>Retour à la liste des diplômes</a>"

    if request.cookies.get('otp') == None or verifCookie(request.cookies.get('otp')):
        # Redirection vers la page de vérification OTP
        return redirect(url_for('verifOTP'))
    # Regénérer le diplome
    cd.creerDiplome(nom, prenom, nomDiplome, timestamp, email)

    # Rediriiger vers la liste des diplomes
    return "Le diplôme a bien été renvoyé" \
           "<br>" \
           "<a href='/'>Retour à l'accueil</a>" \
           "<br>" \
           "<a href='/listeDiplomes'>Voir la liste des diplômes</a>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
