# Utiliser une image Python officielle comme base
FROM python:3.11

# Définir le répertoire de travail dans le container
WORKDIR /app

# Copier tout le projet dans le container
COPY . /app

# Installer les dépendances de l'application
RUN pip install --no-cache-dir -r requirements.txt

# Ajouter le répertoire /app dans le PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application avec Uvicorn
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]