from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <html>
    <head>
    <title>Test</title>
    </head>
    <body>
    <h1>Diplôme digital</h1>
    <a href="/creerDiplome">Créer un diplôme</a>
    <br>
    <a href="/verifDiplom">Vérifier un diplôme</a>
    </body>
    </html>
    """
@app.route("/creerDiplome")
def creerDiplome():
    return """
    <html>
    <head>
    <title>Test</title>
    </head>
    <body>
    <h1>Créer un diplôme</h1>
    <a href="/">Retour</a>
    </body>
    </html>
    """

@app.route("/verifDiplom")
def verifDiplom():
    return """
    <html>
    <head>
    <title>Test</title>
    </head>
    <body>
    <h1>Vérifier un diplôme</h1>
    <a href="/">Retour</a>
    </body>
    </html>
    """

if __name__ == "__main__":
        app.run(host='127.0.0.1', port=8080, debug=True)
