# 🔌 Système de Gestion des Réclamations SENELEC

## 📋 Description

Système de gestion des réclamations pour la Société Nationale d'Électricité du Sénégal (SENELEC). Cette application permet aux clients de soumettre des réclamations et aux administrateurs/techniciens de les traiter efficacement.

## 🚀 Fonctionnalités

### 👥 Gestion des Utilisateurs
- **4 types de rôles :** Admin, Superviseur, Client, Technicien
- **Authentification sécurisée** par email ou téléphone
- **Création automatique de comptes** avec envoi d'emails/SMS
- **Mots de passe temporaires** générés automatiquement

### 🔐 Système d'Authentification
- Connexion via email ou numéro de téléphone
- Redirection automatique selon le rôle utilisateur
- Session management avec Django

### 📧 Notifications Automatiques
- Envoi automatique des credentials par email lors de la création de compte
- Templates d'emails personnalisés
- Support SMTP configurable

### 🛠️ Interface d'Administration
- Interface Django Admin personnalisée
- Gestion complète des utilisateurs et catégories
- Dashboard adapté selon les permissions

## 🏗️ Architecture Technique

### 🔧 Technologies Utilisées
- **Backend :** Python Django 5.0.2
- **Base de Données :** MySQL (SQLite pour dev)
- **APIs :** REST API avec réponses JSON
- **Frontend :** Interface Django Admin + APIs
- **Email :** Django Email Backend (SMTP)

### 📊 Modèles de Données

#### User (Utilisateur Personnalisé)
```python
- id (UUID)
- nom, prenom
- email (unique)
- telephone (unique)
- adresse
- role (admin, superviseur, client, technicien)
- numero_compteur (pour clients)
- temp_password (mot de passe temporaire)
- is_first_login
```

#### Categories
```python
- id (UUID)
- nom (unique)
- description
- is_active
```

#### Reclamation
```python
- id (UUID)
- description
- status (en_attente, en_cours, resolu, ferme, annule)
- dateReponse
- image
- user (ForeignKey)
- categories (ForeignKey)
- technicien (ForeignKey)
```

## 📡 APIs Disponibles

### 🔐 Authentification
- `POST /api/login/` - Connexion utilisateur
- `POST /api/logout/` - Déconnexion
- `GET /api/dashboard/` - Dashboard utilisateur

### 👥 Gestion Utilisateurs (Admin)
- `POST /api/add-user/` - Ajouter un utilisateur
- `POST /api/send-credentials/` - Renvoyer les credentials

### 🏠 Général
- `GET /` - Page d'accueil avec liste des endpoints

## 🛠️ Installation et Configuration

### Prérequis
- Python 3.8+
- MySQL (optionnel, SQLite par défaut)
- Git

### 1. Cloner le Projet
```bash
git clone <repository-url>
cd hackaton-senelec
```

### 2. Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 3. Configuration de la Base de Données

#### Option A: SQLite (Par défaut - Déjà configuré)
Rien à faire, SQLite est déjà configuré pour le développement.

#### Option B: MySQL (Production)
1. Créer la base de données MySQL :
```sql
CREATE DATABASE senelec_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Modifier `senelec_system/settings.py` :
```python
# Décommenter la configuration MySQL et commenter SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'senelec_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. Migrations et Données Initiales
```bash
# Faire les migrations
python manage.py makemigrations
python manage.py migrate

# Créer les données par défaut (utilisateurs et catégories)
python manage.py create_default_data
```

### 5. Configuration Email (Optionnel)
Modifier dans `senelec_system/settings.py` :
```python
EMAIL_HOST_USER = 'votre_email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe_app'
```

### 6. Démarrer le Serveur
```bash
python manage.py runserver
```

Le serveur sera accessible sur `http://127.0.0.1:8000`

## 🧪 Tests avec Postman

Voir le fichier `POSTMAN_TESTS.md` pour un guide complet des tests.

### Comptes par Défaut Créés
- **Admin :** admin@senelec.sn / q77uRwv1
- **Client :** client1@gmail.com / wFUnH2LH
- **Technicien :** technicien1@senelec.sn / zIZtl1sn

## 📁 Structure du Projet

```
hackaton-senelec/
├── senelec_system/          # Configuration Django
│   ├── settings.py          # Paramètres principaux
│   ├── urls.py             # URLs principales
│   └── wsgi.py
├── core/                    # Application principale
│   ├── models.py           # Modèles de données
│   ├── views.py            # Vues API
│   ├── admin.py            # Interface admin
│   ├── urls.py             # URLs de l'app
│   └── management/
│       └── commands/
│           └── create_default_data.py
├── media/                   # Fichiers uploadés
├── requirements.txt         # Dépendances Python
├── README.md               # Ce fichier
├── POSTMAN_TESTS.md        # Guide de tests
└── manage.py               # Script Django
```

## 🔄 Workflow Utilisateur

### 1. Création de Compte (Admin)
1. Admin se connecte sur `/admin/`
2. Admin ajoute un client/technicien via l'API ou l'interface
3. System génère mot de passe temporaire
4. Email automatique envoyé avec credentials

### 2. Première Connexion (Client/Technicien)
1. Utilisateur reçoit email avec credentials
2. Connexion via `/api/login/`
3. Redirection selon rôle :
   - Client/Technicien → Message bienvenue
   - Admin/Superviseur → Dashboard admin

### 3. Gestion des Réclamations (À venir)
- Clients créent des réclamations
- Techniciens traitent les réclamations
- Suivi en temps réel

## 🚀 Prochaines Étapes

### Phase 2 - APIs Réclamations
- [ ] Créer API de soumission de réclamation
- [ ] API de liste des réclamations (filtres par rôle)
- [ ] API d'assignation technicien
- [ ] API de changement de status

### Phase 3 - Interface Utilisateur
- [ ] Interface client (soumission réclamation)
- [ ] Dashboard technicien
- [ ] Dashboard superviseur
- [ ] Interface mobile responsive

### Phase 4 - Fonctionnalités Avancées
- [ ] Notifications push
- [ ] Géolocalisation
- [ ] Rapports et statistiques
- [ ] Intégration SMS

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📞 Support

Pour toute question ou support, contactez l'équipe de développement.

---

**🔋 Développé pour SENELEC - Société Nationale d'Électricité du Sénégal** 