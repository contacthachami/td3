# 🚀 Guide de Déploiement - Flask TODO App

## ⚠️ Pourquoi Netlify ne fonctionne pas ?

**NETLIFY = SITES STATIQUES UNIQUEMENT** (HTML, CSS, JavaScript)  
**VOTRE APP = FLASK (Python) = SERVEUR BACKEND REQUIS**

Netlify ne peut **PAS** exécuter Python/Flask → **404 Error**

---

## ✅ Solution : Déployer sur Render.com

Render est une plateforme gratuite qui supporte Flask et Python.

### 📋 Pré-requis
- Un compte GitHub
- Votre code sur GitHub (déjà fait ✓)
- Un compte Render.com (gratuit)

---

## 🎯 Étapes de Déploiement

### **Option A : Déploiement Automatique (Recommandé)**

#### 1️⃣ Préparer les fichiers (déjà fait ✓)
Les fichiers suivants ont été créés/mis à jour :
- ✅ `render.yaml` - Configuration Render
- ✅ `requirements.txt` - Dépendances avec gunicorn
- ✅ `app.py` - Mis à jour pour production

#### 2️⃣ Pusher les modifications sur GitHub
```powershell
git add .
git commit -m "Add Render deployment configuration"
git push origin main
```

#### 3️⃣ Créer un compte sur Render
- Aller sur https://render.com
- S'inscrire avec GitHub (Sign up with GitHub)
- Autoriser l'accès à vos repositories

#### 4️⃣ Créer un nouveau Web Service
1. Cliquer sur **"New +"** → **"Web Service"**
2. Connecter votre repository GitHub `TD3`
3. Render détectera automatiquement le fichier `render.yaml`
4. Cliquer sur **"Create Web Service"**

#### 5️⃣ Attendre le déploiement
- Le build prend ~2-3 minutes
- Vous verrez les logs en temps réel
- Une fois terminé, vous aurez une URL comme : `https://td3-flask-todo.onrender.com`

---

### **Option B : Configuration Manuelle**

Si le fichier `render.yaml` n'est pas détecté :

1. **New +** → **Web Service**
2. Connecter votre repo GitHub
3. Configurer :
   - **Name**: `td3-flask-todo`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`
4. Cliquer sur **Create Web Service**

---

## 🔧 Commandes Git pour Déployer

```powershell
# Vérifier les modifications
git status

# Ajouter tous les fichiers modifiés
git add .

# Créer un commit
git commit -m "Configure app for Render deployment"

# Pousser vers GitHub
git push origin main
```

---

## 🌐 Autres Plateformes Alternatives

Si Render ne fonctionne pas, vous pouvez essayer :

### **Railway.app**
```bash
# Installer Railway CLI
npm install -g railway

# Se connecter
railway login

# Déployer
railway init
railway up
```

### **PythonAnywhere** (Gratuit pour étudiants)
1. Créer un compte sur https://www.pythonanywhere.com
2. Upload votre code
3. Configurer WSGI file
4. Redémarrer l'app

### **Fly.io**
```bash
# Installer Fly CLI
# Voir : https://fly.io/docs/flyctl/install/

# Se connecter
fly auth login

# Lancer l'app
fly launch
fly deploy
```

---

## 🐛 Dépannage

### **Erreur : "Application failed to start"**
- Vérifier que `gunicorn` est dans `requirements.txt`
- Vérifier la commande de démarrage : `gunicorn app:app`

### **Erreur de base de données**
- Render utilise un stockage éphémère pour le plan Free
- La base SQLite sera réinitialisée à chaque redéploiement
- Solution : Utiliser PostgreSQL (plan payant) ou accepter la réinitialisation

### **404 sur certaines pages**
- Vérifier que toutes les routes sont correctes dans `app.py`
- Tester localement d'abord : `python app.py`

---

## 📱 Tester en Local Avant Déploiement

```powershell
# Installer toutes les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py

# Ouvrir dans le navigateur
# http://127.0.0.1:5000
```

---

## ✨ Résumé Rapide

1. ❌ **Netlify** → Ne supporte pas Flask (sites statiques uniquement)
2. ✅ **Render** → Supporte Flask (gratuit)
3. 📁 Les fichiers ont été créés automatiquement
4. 🔄 Git push → Render détecte et déploie automatiquement
5. 🌐 Vous obtenez une URL publique fonctionnelle

---

## 🎓 Pour Plus d'Informations

- [Documentation Render Python](https://render.com/docs/deploy-flask)
- [Documentation Flask Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

**Bon déploiement ! 🚀**
