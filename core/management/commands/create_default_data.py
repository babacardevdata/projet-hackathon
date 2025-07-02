from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import User, Categories
import random
import string


class Command(BaseCommand):
    help = 'Crée les données par défaut pour le système SENELEC'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Supprimer toutes les données existantes avant de créer les nouvelles',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Suppression des données existantes...')
            User.objects.all().delete()
            Categories.objects.all().delete()

        self.stdout.write('🚀 Création des données par défaut...')

        # Créer les catégories par défaut
        categories_data = [
            {'nom': 'Panne Électrique', 'description': 'Problèmes liés aux coupures et pannes électriques'},
            {'nom': 'Facturation', 'description': 'Questions et problèmes de facturation'},
            {'nom': 'Compteur', 'description': 'Problèmes avec les compteurs électriques'},
            {'nom': 'Raccordement', 'description': 'Demandes de nouveau raccordement'},
            {'nom': 'Qualité Service', 'description': 'Plaintes sur la qualité du service'},
            {'nom': 'Autre', 'description': 'Autres types de réclamations'},
        ]

        categories_created = []
        for cat_data in categories_data:
            category, created = Categories.objects.get_or_create(
                nom=cat_data['nom'],
                defaults={'description': cat_data['description']}
            )
            if created:
                categories_created.append(category)
                self.stdout.write(f'✅ Catégorie créée: {category.nom}')

        # Générer un mot de passe aléatoire
        def generate_temp_password(length=8):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for _ in range(length))

        # Créer les utilisateurs par défaut
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@senelec.sn',
                'nom': 'Administrateur',
                'prenom': 'Système',
                'telephone': '221771234567',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'adresse': 'Siège SENELEC, Dakar'
            },
            {
                'username': 'supervisor',
                'email': 'supervisor@senelec.sn',
                'nom': 'Diop',
                'prenom': 'Superviseur',
                'telephone': '221772234567',
                'role': 'superviseur',
                'is_staff': True,
                'adresse': 'Bureau SENELEC, Dakar'
            },
            {
                'username': 'technicien1',
                'email': 'technicien1@senelec.sn',
                'nom': 'Sarr',
                'prenom': 'Moussa',
                'telephone': '221773234567',
                'role': 'technicien',
                'adresse': 'Atelier SENELEC, Pikine'
            },
            {
                'username': 'technicien2',
                'email': 'technicien2@senelec.sn',
                'nom': 'Fall',
                'prenom': 'Aminata',
                'telephone': '221774234567',
                'role': 'technicien',
                'adresse': 'Atelier SENELEC, Guédiawaye'
            },
            {
                'username': 'client1',
                'email': 'client1@gmail.com',
                'nom': 'Ndiaye',
                'prenom': 'Ibrahima',
                'telephone': '221775234567',
                'role': 'client',
                'numero_compteur': 'CPT-001-2024',
                'adresse': 'Cité Keur Gorgui, Dakar'
            },
            {
                'username': 'client2',
                'email': 'client2@gmail.com',
                'nom': 'Ba',
                'prenom': 'Fatou',
                'telephone': '221776234567',
                'role': 'client',
                'numero_compteur': 'CPT-002-2024',
                'adresse': 'Médina, Dakar'
            },
            {
                'username': 'client3',
                'email': 'client3@yahoo.fr',
                'nom': 'Sow',
                'prenom': 'Mamadou',
                'telephone': '221777234567',
                'role': 'client',
                'numero_compteur': 'CPT-003-2024',
                'adresse': 'Parcelles Assainies, Dakar'
            }
        ]

        users_created = []
        for user_data in users_data:
            # Générer un mot de passe temporaire
            temp_pass = generate_temp_password()
            
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'nom': user_data['nom'],
                    'prenom': user_data['prenom'],
                    'telephone': user_data['telephone'],
                    'role': user_data['role'],
                    'adresse': user_data.get('adresse', ''),
                    'numero_compteur': user_data.get('numero_compteur', ''),
                    'password': make_password(temp_pass),
                    'temp_password': temp_pass,
                    'is_staff': user_data.get('is_staff', False),
                    'is_superuser': user_data.get('is_superuser', False),
                    'is_active': True,
                }
            )
            
            if created:
                users_created.append((user, temp_pass))
                self.stdout.write(
                    f'✅ Utilisateur créé: {user.get_full_name()} ({user.role}) - '
                    f'Email: {user.email} - Mot de passe: {temp_pass}'
                )

        # Résumé
        self.stdout.write('\n📊 RÉSUMÉ:')
        self.stdout.write(f'   - {len(categories_created)} catégories créées')
        self.stdout.write(f'   - {len(users_created)} utilisateurs créés')
        
        self.stdout.write('\n🔑 INFORMATIONS DE CONNEXION:')
        for user, password in users_created:
            self.stdout.write(f'   {user.role.upper()}: {user.email} / {password}')
        
        self.stdout.write('\n✨ Données par défaut créées avec succès!')
        self.stdout.write('💡 Vous pouvez maintenant tester l\'authentification avec ces comptes.') 