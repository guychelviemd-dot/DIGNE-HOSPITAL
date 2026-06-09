# 🚂 Déploiement sur Railway.app — SGHL

## 📋 Prérequis

- Compte GitHub
- Compte [Railway.app](https://railway.app)
- Projet SGHL prêt à déployer

---

## 🏗️ Architecture du Déploiement

```
┌─────────────────────────────────────────────────┐
│           RAILWAY.APP SERVICES                  │
├─────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐              │
│  │   Frontend  │  │   Backend    │              │
│  │   (Vue.js)  │  │   (Django)   │              │
│  │  Port 80    │  │  Port 8000   │              │
│  └──────┬──────┘  └──────┬───────┘              │
│         │                │                      │
│         └────────┬───────┘                      │
│                  │                              │
│         ┌────────▼────────┐  ┌─────────────┐   │
│         │   PostgreSQL    │  │    Redis    │   │
│         │   (Database)    │  │   (Cache)   │   │
│         └─────────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Étape 1: Préparer le Projet

### 1.1 Installer Railway CLI (Optionnel)

```bash
npm i -g @railway/cli
```

### 1.2 Créer les Fichiers de Configuration

#### **Fichier `railway.json` à la racine** (optionnel)

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi:application",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## 🌐 Étape 2: Déployer le Backend (Django)

### 2.1 Créer un Nouveau Projet sur Railway

1. Connectez-vous à [Railway.app](https://railway.app)
2. Cliquez sur **"New Project"**
3. Sélectionnez **"Deploy from GitHub repo"**
4. Choisissez votre dépôt SGHL

### 2.2 Créer un Service Backend

```
1. Click "+" → "New Service"
2. Select "GitHub" → Choose repo
3. Select directory: ./backend
4. Name it: "sghl-backend"
```

### 2.3 Configurer les Variables d'Environnement

Dans l'onglet **"Variables"** du service backend :

```env
# Django Settings
DEBUG=False
SECRET_KEY=generate-a-random-secret-key-here
ALLOWED_HOSTS=*.railway.app,localhost,127.0.0.1

# Database (Railway fournit ces variables automatiquement)
DATABASE_URL=${{DATABASE_URL}}

# Redis (Railway fournit cette variable)
REDIS_URL=${{REDIS_URL}}

# Email (Gmail SMTP)
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password

# Security
CSRF_TRUSTED_ORIGINS=https://*.railway.app
CORS_ALLOWED_ORIGINS=https://*.railway.app
```

### 2.4 Configurer le Build

Dans l'onglet **"Settings"** → **"Build & Run Commands"** :

```
Build Command: pip install -r requirements.txt
Start Command: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi:application
```

### 2.5 Ajouter PostgreSQL

```
1. Dans le projet Railway, cliquez sur "+ New"
2. Choisissez "Database" → "PostgreSQL"
3. Nommez-le: "sghl-db"
4. Connectez-le au service backend
```

Railway ajoutera automatiquement `DATABASE_URL` aux variables d'environnement.

### 2.6 Ajouter Redis

```
1. Cliquez sur "+ New"
2. Choisissez "Database" → "Redis"
3. Nommez-le: "sghl-redis"
4. Connectez-le au service backend
```

Railway ajoutera automatiquement `REDIS_URL` aux variables d'environnement.

### 2.7 Déployer

```bash
# Railway déploie automatiquement après chaque push Git
# Pour forcer un déploiement :
git push railway main
```

### 2.8 Vérifier le Backend

Une fois déployé, notez l'URL du backend :
```
https://sghl-backend-production-xxxx.up.railway.app
```

Testez l'API :
```bash
curl https://sghl-backend-production-xxxx.up.railway.app/api/v1/dashboard/health
```

---

## 🎨 Étape 3: Déployer le Frontend (Vue.js)

### 3.1 Créer un Service Frontend

```
1. Dans le même projet Railway, cliquez sur "+ New"
2. Select "GitHub" → Choose repo
3. Select directory: ./frontend
4. Name it: "sghl-frontend"
```

### 3.2 Configurer les Variables d'Environnement

```env
# URL du backend (remplacez par votre URL Railway)
VITE_API_BASE_URL=https://sghl-backend-production-xxxx.up.railway.app

# Build settings
NODE_VERSION=18
```

### 3.3 Configurer le Build

Dans **"Settings"** → **"Build & Run Commands"** :

```
Build Command: npm install && npm run build
Start Command: npx serve -s dist -p $PORT
```

### 3.4 Ajouter le Port Dynamique

Créez/modifiez `frontend/serve.js` :

```javascript
const serve = require('serve');
const port = process.env.PORT || 3000;
serve('./dist', { port });
```

### 3.5 Mettre à Jour `package.json`

Ajoutez dans les scripts :

```json
{
  "scripts": {
    "serve": "npx serve -s dist -p $PORT"
  },
  "dependencies": {
    "serve": "^14.2.0"
  }
}
```

### 3.6 Déployer

```bash
git push
```

---

## 🔗 Étape 4: Configurer la Communication Frontend ↔ Backend

### 4.1 Mettre à Jour `vite.config.js`

```javascript
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
```

### 4.2 Mettre à Jour `src/services/api.js`

```javascript
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  }
})
```

---

## 🔐 Étape 5: Configuration Production

### 5.1 Django Settings Production

Créez `backend/core/settings_production.py` :

```python
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['*.railway.app', 'localhost', '127.0.0.1']

CORS_ALLOWED_ORIGINS = [
    "https://sghl-frontend-production-xxxx.up.railway.app",
]

CSRF_TRUSTED_ORIGINS = [
    "https://sghl-frontend-production-xxxx.up.railway.app",
]

# Database (utilisé via DATABASE_URL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 5.2 Migrate & Collectstatic

```bash
# Exécuter dans Railway Shell (Web Terminal)
python manage.py migrate
python manage.py collectstatic --noinput
```

---

## 📊 Étape 6: Vérifications Post-Déploiement

### 6.1 Tester le Backend

```bash
# Health check
curl https://sghl-backend-production-xxxx.up.railway.app/api/v1/dashboard/health

# API Docs
curl https://sghl-backend-production-xxxx.up.railway.app/api/v1/docs/
```

### 6.2 Tester le Frontend

Ouvrez dans le navigateur :
```
https://sghl-frontend-production-xxxx.up.railway.app
```

### 6.3 Vérifier la Base de Données

```bash
# Railway Shell
railway open
psql $DATABASE_URL
```

---

## 🎯 URLs Finales

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | `https://sghl-frontend-production-xxxx.up.railway.app` | Interface utilisateur |
| **Backend API** | `https://sghl-backend-production-xxxx.up.railway.app` | API REST |
| **Admin** | `https://sghl-backend-production-xxxx.up.railway.app/admin/` | Panel admin |
| **API Docs** | `https://sghl-backend-production-xxxx.up.railway.app/api/v1/docs/` | Swagger |

---

## 🔧 Commandes Utiles Railway

```bash
# Ouvrir le shell à distance
railway shell

# Voir les logs
railway logs

# Ouvrir le dashboard
railway open

# Afficher les variables
railway variables

# Déployer une branche spécifique
railway deploy --branch=develop

# Afficher les détails du service
railway status
```

---

## 💰 Coûts Railway

- **Gratuit** : 500 heures/mois (~20 jours de fonctionnement)
- **PostgreSQL** : Inclus dans le plan gratuit (avec limites)
- **Redis** : Inclus dans le plan gratuit (avec limites)
- **Bandwidth** : 5GB/mois gratuit

Pour une application de production, prévoyez **~5$/mois** par service.

---

## 🐛 Dépannage

### Problème: Build échoue

```bash
# Vérifier les logs
railway logs

# Tester localement
cd backend
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

### Problème: Database connection

```python
# Vérifier DATABASE_URL
echo $DATABASE_URL

# Tester connexion
python manage.py dbshell
```

### Problème: CORS errors

```python
# Dans settings.py
CORS_ALLOWED_ORIGINS = [
    "https://votre-frontend.railway.app",
]
```

### Problème: Static files 404

```bash
# Exécuter collectstatic
python manage.py collectstatic --noinput

# Vérifier STATIC_ROOT
ls staticfiles/
```

---

## 📚 Ressources

- [Railway Documentation](https://docs.railway.app)
- [Django on Railway](https://docs.railway.app/guides/django)
- [Vue.js on Railway](https://docs.railway.app/guides/node)

---

## ✅ Checklist de Déploiement

- [ ] Backend déployé et accessible
- [ ] Frontend déployé et accessible
- [ ] PostgreSQL configuré
- [ ] Redis configuré
- [ ] Variables d'environnement définies
- [ ] Migrations exécutées
- [ ] Static files collectés
- [ ] Superuser créé
- [ ] CORS configuré
- [ ] Health check fonctionne
- [ ] API répond correctement

---

**Développé avec ❤️ par NLP-Core-Team**
