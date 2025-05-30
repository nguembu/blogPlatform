# Utilise une image officielle Python comme image de base
FROM python:3.14-slim-bookworm

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances en premier pour optimiser le cache Docker
COPY requirements.txt .

# Met à jour les paquets système pour corriger les vulnérabilités
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port sur lequel l'application va tourner (ex: 8000)
EXPOSE 8000

# Commande pour démarrer l'application Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]