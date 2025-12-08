# 1. Image de base
FROM mirror.gcr.io/library/python:3.11-slim

# 2. Définir le répertoire de travail
WORKDIR /app

# 3. Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "dvc[gdrive]==3.63.0"

# 4. Copier tout le code du projet
COPY . .

# 5. Définir la commande par défaut pour exécuter la pipeline DVC
CMD ["dvc", "repro", "-v"]

