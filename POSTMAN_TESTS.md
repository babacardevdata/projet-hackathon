# 🧪 Guide de Tests POSTMAN - Système SENELEC

## 📋 Configuration de Base

**Base URL:** `http://127.0.0.1:8000`

## 🔐 Informations de Connexion par Défaut

Les comptes suivants ont été créés automatiquement :

### 👨‍💼 Admin
- **Email:** `admin@senelec.sn`
- **Mot de passe:** `q77uRwv1`
- **Rôle:** admin

### 👨‍💼 Superviseur
- **Email:** `supervisor@senelec.sn`
- **Mot de passe:** `A2ABzFab`
- **Rôle:** superviseur

### 🔧 Techniciens
1. **Email:** `technicien1@senelec.sn` / **Mot de passe:** `zIZtl1sn`
2. **Email:** `technicien2@senelec.sn` / **Mot de passe:** `iXLo9zoQ`

### 👤 Clients
1. **Email:** `client1@gmail.com` / **Mot de passe:** `wFUnH2LH`
2. **Email:** `client2@gmail.com` / **Mot de passe:** `bSaPRWtp`
3. **Email:** `client3@yahoo.fr` / **Mot de passe:** `boqn71sl`

---

## 🧪 Tests à Effectuer

### 1. 🏠 Test de l'API d'Accueil

**Endpoint:** `GET /`

**Description:** Vérifier que le serveur fonctionne

**Réponse attendue:**
```json
{
    "message": "Bienvenue sur l'API SENELEC",
    "endpoints": {
        "login": "/api/login/",
        "logout": "/api/logout/",
        "add_user": "/api/add-user/",
        "send_credentials": "/api/send-credentials/",
        "dashboard": "/api/dashboard/",
        "dashboard_stats": "/api/dashboard/statistiques-generales/"
    }
}
```

---

### 2. 🔐 Test de Connexion (Login)

**Endpoint:** `POST /api/login/`

**Headers:**
```
Content-Type: application/json
```

#### Test 1: Connexion Admin (Succès)
**Body:**
```json
{
    "email_or_phone": "admin@senelec.sn",
    "password": "q77uRwv1"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Redirection vers le dashboard administrateur...",
    "user": {
        "id": "uuid",
        "nom": "Administrateur",
        "prenom": "Système",
        "email": "admin@senelec.sn",
        "role": "admin",
        "is_first_login": true
    },
    "dashboard_url": "/admin/"
}
```

#### Test 2: Connexion Client (Succès)
**Body:**
```json
{
    "email_or_phone": "client1@gmail.com",
    "password": "wFUnH2LH"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Bienvenue Ibrahima Ndiaye! Connexion réussie.",
    "user": {
        "id": "uuid",
        "nom": "Ndiaye",
        "prenom": "Ibrahima",
        "email": "client1@gmail.com",
        "role": "client",
        "is_first_login": true
    },
    "dashboard_url": "/dashboard/"
}
```

#### Test 3: Connexion avec Téléphone
**Body:**
```json
{
    "email_or_phone": "221775234567",
    "password": "wFUnH2LH"
}
```

#### Test 4: Connexion Échec (Mauvais mot de passe)
**Body:**
```json
{
    "email_or_phone": "admin@senelec.sn",
    "password": "mauvais_mot_de_passe"
}
```

**Réponse attendue:**
```json
{
    "success": false,
    "message": "Email/téléphone ou mot de passe incorrect"
}
```

---

### 3. 📊 Test du Dashboard

**Endpoint:** `GET /api/dashboard/`

**Prérequis:** Être connecté (utilisez les cookies de session de la connexion précédente)

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Bienvenue sur votre dashboard, Prénom Nom!",
    "user": {
        "nom": "Nom",
        "prenom": "Prénom",
        "role": "role",
        "email": "email@example.com"
    }
}
```

---

### 4. 📊 Test des Statistiques Dashboard

**Endpoint:** `GET /api/dashboard/statistiques-generales/`

**Prérequis:** Être connecté

#### Test Admin/Superviseur :
**Réponse attendue:**
```json
{
    "success": true,
    "message": "Statistiques pour Système Administrateur",
    "user_role": "admin",
    "statistics": {
        "total_users": 7,
        "total_clients": 3,
        "total_techniciens": 2,
        "total_categories": 6,
        "total_reclamations": 0,
        "reclamations_en_attente": 0,
        "reclamations_en_cours": 0,
        "reclamations_resolues": 0
    }
}
```

#### Test Client :
**Réponse attendue:**
```json
{
    "success": true,
    "message": "Statistiques pour Ibrahima Ndiaye",
    "user_role": "client",
    "statistics": {
        "mes_reclamations": 0,
        "en_attente": 0,
        "en_cours": 0,
        "resolues": 0
    }
}
```

---

### 5. ➕ Test d'Ajout d'Utilisateur (Admin uniquement)

**Endpoint:** `POST /api/add-user/`

**Prérequis:** Être connecté en tant qu'admin

**Headers:**
```
Content-Type: application/json
```

#### Test 1: Ajout Client (Succès)
**Body:**
```json
{
    "nom": "Test",
    "prenom": "Nouveau",
    "email": "nouveau.client@test.com",
    "telephone": "221700000001",
    "role": "client",
    "adresse": "Adresse test, Dakar",
    "numero_compteur": "CPT-TEST-001"
}
```

#### Test 2: Ajout Technicien (Succès)
**Body:**
```json
{
    "nom": "Technicien",
    "prenom": "Nouveau",
    "email": "nouveau.technicien@senelec.sn",
    "telephone": "221700000002",
    "role": "technicien",
    "adresse": "Atelier SENELEC, Test"
}
```

#### Test 3: Tentative sans être admin (Échec)
*Se connecter d'abord avec un compte client, puis essayer d'ajouter un utilisateur*

**Réponse attendue:**
```json
{
    "success": false,
    "message": "Accès non autorisé. Admin requis."
}
```

---

### 6. 📧 Test d'Envoi des Informations de Connexion

**Endpoint:** `POST /api/send-credentials/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
    "email": "client1@gmail.com"
}
```

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Informations de connexion envoyées à client1@gmail.com",
    "email_sent": true
}
```

---

### 7. 🚪 Test de Déconnexion

**Endpoint:** `POST /api/logout/`

**Prérequis:** Être connecté

**Réponse attendue:**
```json
{
    "success": true,
    "message": "Déconnexion réussie"
}
```

---

## 🔍 Tests d'Erreurs à Vérifier

### 1. Champs Manquants
- Connexion sans email/téléphone
- Connexion sans mot de passe
- Ajout d'utilisateur avec champs manquants

### 2. Utilisateurs Inexistants
- Connexion avec email inexistant
- Envoi de credentials à email inexistant

### 3. Doublons
- Créer utilisateur avec email existant
- Créer utilisateur avec téléphone existant

### 4. Accès Non Autorisé
- Accéder au dashboard sans être connecté
- Ajouter utilisateur sans être admin

---

## 📝 Ordre de Tests Recommandé

1. ✅ **Test d'Accueil** - Vérifier que le serveur fonctionne
2. ✅ **Connexion Admin** - Se connecter avec l'admin
3. ✅ **Dashboard Admin** - Vérifier l'accès au dashboard
4. ✅ **Statistiques Admin** - Tester les statistiques générales
5. ✅ **Ajout de Client** - Créer un nouveau client
6. ✅ **Ajout de Technicien** - Créer un nouveau technicien
7. ✅ **Envoi Credentials** - Envoyer les infos à un utilisateur
8. ✅ **Déconnexion** - Se déconnecter
9. ✅ **Connexion Client** - Se connecter avec un client
10. ✅ **Dashboard Client** - Vérifier l'accès client
11. ✅ **Statistiques Client** - Tester les statistiques client
12. ✅ **Tests d'Erreurs** - Vérifier la gestion des erreurs

---

## 💡 Notes Importantes

- **Cookies de Session:** Postman doit conserver les cookies entre les requêtes pour maintenir la session
- **CSRF:** Les APIs sont exemptées de CSRF pour faciliter les tests
- **Email:** Les emails ne seront envoyés que si SMTP est configuré dans settings.py
- **Base de Données:** Actuellement en SQLite, à migrer vers MySQL plus tard

---

**🎯 Résultat Attendu:** Toutes les APIs doivent répondre correctement selon leur rôle et permissions ! 