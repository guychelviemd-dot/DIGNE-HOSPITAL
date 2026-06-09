# 🚂 Guide de Déploiement sur Railway.app

## 📌 Résumé

Ce guide vous explique comment déployer votre application SGHL sur **Railway.app** en 5 étapes simples.

---

## ✅ Prérequis

1. **Compte GitHub** (déjà créé)
2. **Compte Railway.app** - [Inscription gratuite](https://railway.app)
3. **Projet SGHL** sur GitHub

---

## 🚀 Étape 1: Préparer le Projet

Les fichiers de configuration nécessaires ont été créés :

- ✅ `railway.json` - Configuration Railway
- ✅ `backend/NIXPACKS.toml` - Build backend
- ✅ `frontend/NIXPACKS.toml` - Build frontend
- ✅ `frontend/.env.example` - Variables frontend
- ✅ `README_RAILWAY.md` - Documentation complète

---

## 🌐 Étape 2: Créer un Projet sur Railway

1. **Connectez-vous** à [Railway.app](https://railway.app)
2. **Cliquez sur "New Project"**
3. **Choisissez "Deploy from GitHub repo"**
4. **Sélectionnez votre dépôt SGHL**

---

## 🔧 Étape 3: Déployer le Backend

### 3.1 Créer le Service Backend

```
1. Dans le projet Railway, cliquez sur "+ New"
2. Choisissez "GitHub Repo"
3. Sélectionnez votre dépôt
4. Dans "Directory", mettez: ./backend
5. Nommez le service: "sghl-backend"
```

### 3.2 Ajouter la Base de Données PostgreSQL

```
1. Cliquez sur "+ New" dans le projet
2. Choisissez "Database" → "PostgreSQL"
3. Nommez-la: "sghl-db"
4. Railway génère automatiquement DATABASE_URL
```

### 3.3 Ajouter Redis

```
1. Cliquez sur "+ New"
2. Choisissez "Database" → "Redis"
3. Nommez-le: "sghl-redis"
4. Railway génère automatiquement REDIS_URL
```

### 3.4 Configurer les Variables d'Environnement

Dans l'onglet **"Variables"** du service backend, ajoutez :

```env
# Django Settings
DEBUG=False
SECRET_KEY=generate-a-random-secret-key-here
ALLOWED_HOSTS=*.railway.app,localhost,127.0.0.1

# Email (Gmail SMTP)
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password-gmail

# CORS & CSRF
CORS_ALLOWED_ORIGINS=https://*.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app

# Media & Static
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_NAME=
```

> **💡 Générer un SECRET_KEY :**
> ```python
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 3.5 Configurer le Build

Dans **"Settings"** → **"Build & Run Commands"** :

```
Build Command: pip install -r requirements.txt
Start Command: python manage.py migrate && python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### 3.6 Déployer

Railway déploie automatiquement après chaque push Git.

**URL du backend :** `https://sghl-backend-production-xxxx.up.railway.app`

---

## 🎨 Étape 4: Déployer le Frontend

### 4.1 Créer le Service Frontend

```
1. Cliquez sur "+ New"
2. Choisissez "GitHub Repo"
3. Sélectionnez votre dépôt
4. Dans "Directory", mettez: ./frontend
5. Nommez le service: "sghl-frontend"
```

### 4.2 Configurer les Variables d'Environnement

```env
VITE_API_BASE_URL=https://sghl-backend-production-xxxx.up.railway.app
```

### 4.3 Configurer le Build

```
Build Command: npm ci && npm run build
Start Command: npx serve -s dist -p $PORT
```

### 4.4 Déployer

**URL du frontend :** `https://sghl-frontend-production-xxxx.up.railway.app`

---

## 🔗 Étape 5: Finaliser la Configuration

### 5.1 Mettre à Jour les Variables

Dans le service **backend**, ajoutez :

```env
CORS_ALLOWED_ORIGINS=https://sghl-frontend-production-xxxx.up.railway.app
CSRF_TRUSTED_ORIGINS=https://sghl-frontend-production-xxxx.up.railway.app
```

### 5.2 Exécuter les Migrations

```bash
# Via Railway Shell
railway shell
python manage.py migrate
python manage.py createsuperuser
```

### 5.3 Vérifier le Déploiement

```bash
# Health check backend
curl https://sghl-backend-production-xxxx.up.railway.app/api/v1/dashboard/health

# Ouvrir le frontend
https://sghl-frontend-production-xxxx.up.railway.app
```

---

## 📊 URLs Finales

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | `https://sghl-frontend-production-xxxx.up.railway.app` | Interface utilisateur |
| **Backend API** | `https://sghl-backend-production-xxxx.up.railway.app` | API REST |
| **Admin** | `https://sghl-backend-production-xxxx.up.railway.app/admin/` | Panel admin |

---

## 🐛 Dépannage

### Problème: Build échoue

```bash
# Voir les logs
railway logs

# Tester localement
cd backend
pip install -r requirements.txt
python manage.py collectstatic --noinput
```

### Problème: CORS Error

```python
# Dans backend/core/settings.py
CORS_ALLOWED_ORIGINS = [
    "https://sghl-frontend-production-xxxx.up.railway.app",
]
```

### Problème: Database Connection

```bash
# Vérifier DATABASE_URL
railway variables

# Tester connexion
railway shell
python manage.py dbshell
```

---

## 💰 Coûts

- **Gratuit** : 500 heures/mois (~20 jours)
- **PostgreSQL** : Inclus (limité)
- **Redis** : Inclus (limité)
- **Bandwidth** : 5GB/mois

**Pour production : ~10-15$/mois**

---

## ✅ Checklist

- [ ] Backend déployé
- [ ] Frontend déployé
- [ ] PostgreSQL connecté
- [ ] Redis connecté
- [ ] Variables d'environnement définies
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] CORS configuré
- [ ] Health check fonctionne
- [ ] Frontend connecte au backend

---

## 📚 Ressources

- [Documentation Railway](https://docs.railway.app)
- [Guide complet](README_RAILWAY.md)
- [Support Railway](https://railway.app/discord)

---

**Développé avec ❤️ par NLP-Core-Team**
