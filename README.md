# 📝 BlogPlatform

BlogPlatform est une application web de blogging développée avec **Django**. Elle permet aux utilisateurs de créer, modifier et supprimer des articles, ainsi que de consulter des publications. Le projet est conteneurisé avec Docker pour faciliter le déploiement.

Note: Cliquez sur ce lien pour accéder a l'application:  https://blogplatform-qcbo.onrender.com/

## 🚀 Fonctionnalités

- ✏️ Création et édition d’articles de blog
- 💬 Système de commentaires
- 🔐 Interface d’administration via Django Admin
- 🐳 Déploiement simplifié avec Docker
- 🔄 Détection de signaux (`signals.py`)
- 🧾 Formulaires Django (`forms.py`)

## 📁 Structure du projet


## 🛠️ Technologies utilisées

- [Python 3.10+](https://www.python.org/)
- [Django 4.x](https://www.djangoproject.com/)
- [Pillow](https://python-pillow.org/) (gestion des images)
- [Docker](https://www.docker.com/)
- [SQLite](https://www.sqlite.org/index.html)

---

## ⚙️ Installation en local

### 1. Cloner le projet

bash
git clone https://github.com/nguembu/blogplatform.git
cd blogplatform```

### 2. Créer un environnement virtuel (recommandé)
python -m venv env
source env/bin/activate  # Linux/macOS
env\\Scripts\\activate   # Windows

### 3. Installer les dépendances
pip install -r requirements.txt

#### 4. Lancer les migrations et le serveur
python manage.py migrate
python manage.py runserver

## 🐳 Déploiement avec Docker
### 1. Construire et lancer les conteneurs
docker-compose up --build
### 2. Accès à l’application
Ouvre ton navigateur à l’adresse :
http://localhost:8000

## 📦 Variables d’environnement
Crée un fichier .env à la racine du projet pour y stocker :
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1



