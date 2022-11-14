from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

import stegano as stg
import creerDiplome as cd
import verifDiplome as vd

app = Flask(__name__)

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
    </body>
    </html>
    """

@app.route('/creerDiplome', methods=['GET', 'POST'])
def creerDiplome():
    # TODO : Rajouter l'OTP

    if request.method == 'POST':
        # Récupérer les valeurs du formulaire
        if request.form['nom'] and request.form['prenom'] and request.form['nomDiplome']:
            nom = request.form['nom']
            prenom = request.form['prenom']
            nomDiplome = request.form['nomDiplome']
            # get timestamp
            # TODO Certifier le timestamp
            now = datetime.now()
            timestamp = str(round(datetime.timestamp(now)))
            print("timestamp =", timestamp)
        #sinon on revoie une erreur
        else:
            return "Erreur, veuillez remplir tous les champs"

        cd.creerDiplome(nom, prenom, nomDiplome, timestamp)

        # Insérer les valeurs dans un fichier texte
        with open('diplome/diplomeCree/diplomes.txt', 'a') as f:
            f.write(nom + ' ' + prenom + ' ' + nomDiplome + ' ' +timestamp +'\n')

        return redirect(url_for('listeDiplomes'))
    else:
        return render_template('creerDiplome.html')


@app.route('/listeDiplomes')
def listeDiplomes():
    # Lire le fichier texte et stocker dans une liste de diplomes
    diplomes = []
    with open('diplome/diplomeCree/diplomes.txt', 'r') as f:
        for line in f:
            nom, prenom, nomDiplome, timestamp = line.split(' ')
            diplomes.append({'nom': nom, 'prenom': prenom, 'nomDiplome': nomDiplome, 'timestamp': timestamp})
    return render_template('listeDiplomes.html', diplomes=diplomes)

# Verfier le fichier uploadé
@app.route('/verifDiplome', methods=['GET', 'POST'])
def verifDiplom():
    if request.method == 'POST':
        # Récupérer le fichier uploadé
        f = request.files['file']
        # Sauvegarder le fichier dans le dossier upload
        f.save('diplome/uploads/' + f.filename)
        vd.verifDiplome(f.filename)

        return redirect(url_for('listeDiplomes'))
    else:
        return render_template('verifDiplome.html')




if __name__ == "__main__":
        app.run(host='127.0.0.1', port=8080, debug=True)