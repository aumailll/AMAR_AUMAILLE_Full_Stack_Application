# Utiliser une image Python officielle comme base
FROM python:3.11

# Définir le répertoire de travail dans le container
WORKDIR /app

# Copier les fichiers nécessaires dans le container (ici tout le projet, y compris api)
COPY . /app

# Installer les dépendances de l'application (si tu as un requirements.txt)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Exposer le port 8000
EXPOSE 8000

ENV PYTHONPATH=/app

# Commande pour lancer l'application avec Uvicorn (serveur ASGI pour FastAPI)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
