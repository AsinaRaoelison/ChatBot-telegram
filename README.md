# meteo-telegram

# Bot Météo Telegram

Ce projet est un bot Telegram qui fournit des mises à jour météo quotidiennes pour une certaine localisation. Le bot utilise l'API OpenWeatherMap pour récupérer les données météorologiques.

## Fonctionnalités

- Envoi de mises à jour météo quotidiennes à 8h00 (heure locale).
- Possibilité de s'abonner et de se désabonner des mises à jour.
- Utilisation d'un clavier en ligne pour gérer les abonnements.

## Configuration

1. Clonez ce référentiel sur votre ordinateur :

    git clone https://github.com/votre-nom-utilisateur/votre-nom-repo.git

2. Installez les dépendances nécessaires en exécutant :

pip install -r requirements.txt


3. Obtenez une clé API OpenWeatherMap en vous inscrivant sur leur site : https://openweathermap.org/appid

4. Configurez votre bot Telegram en créant un nouveau bot via le BotFather : https://core.telegram.org/bots#botfather

5. Créez un fichier `config.py` dans le même répertoire que votre code avec les informations suivantes :

```python
    API_KEY_OPENWEATHERMAP = "votre_clé_api_openweathermap"
    BOT_TOKEN = "votre_token_bot_telegram"
    Exécutez votre bot en utilisant la commande suivante :
    python votre_script.py

