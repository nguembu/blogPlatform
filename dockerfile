# Utilise une image officielle Python comme image de base
FROM python:3.12-slim-bookworm

# Update system packages to fix vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port sur lequel l'application va tourner (ex: 8000)
EXPOSE 8000

# Commande pour démarrer l'application (à adapter selon votre framework)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]