# Image légère pour Python
FROM python:3.11-slim

# Empêche Python de générer des fichiers .pyc et permet l'affichage des logs en temps réel
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Installation des dépendances inscrites dans le fichier requirement.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

# On rend notre conteneur accessuble depuis le port 8000
EXPOSE 8000

# On lance Uvicorn en pointant vers le fichier Server.py dans le dossier Server (script qui utiliser FastAPI)
# Format: dossier.fichier:variable_fastapi
CMD ["uvicorn", "Server.Server:app", "--host", "0.0.0.0", "--port", "8000"]