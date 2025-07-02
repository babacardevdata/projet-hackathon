from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View
import json
import random
import string
from .models import User, Categories, Reclamation


def generate_temp_password(length=8):
    """Génère un mot de passe temporaire aléatoire"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def send_credentials_email(user, temp_password):
    """Envoie les informations de connexion par email"""
    subject = 'Vos informations de connexion - Système SENELEC'
    message = f"""
    Bonjour {user.get_full_name()},

    Voici vos informations de connexion au système SENELEC :

    📧 Email : {user.email}
    🔑 Mot de passe temporaire : {temp_password}
    👤 Rôle : {user.get_role_display()}

    Veuillez vous connecter et modifier votre mot de passe lors de votre première connexion.

    Cordialement,
    L'équipe SENELEC
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False


@csrf_exempt
@require_http_methods(["POST"])
def login_api(request):
    """API de connexion des utilisateurs"""
    try:
        data = json.loads(request.body)
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')
        
        if not email_or_phone or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email/téléphone et mot de passe requis'
            }, status=400)
        
        # Chercher l'utilisateur par email ou téléphone
        user = None
        try:
            if '@' in email_or_phone:
                user = User.objects.get(email=email_or_phone)
            else:
                user = User.objects.get(telephone=email_or_phone)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }, status=404)
        
        # Vérifier le mot de passe
        user_auth = authenticate(request, username=user.email, password=password)
        if user_auth:
            login(request, user_auth)
            
            # Déterminer la redirection selon le rôle
            if user.role in ['admin', 'superviseur']:
                redirect_message = "Redirection vers le dashboard administrateur..."
                dashboard_url = "/admin/"
            else:
                redirect_message = f"Bienvenue {user.get_full_name()}! Connexion réussie."
                dashboard_url = "/dashboard/"
            
            return JsonResponse({
                'success': True,
                'message': redirect_message,
                'user': {
                    'id': str(user.id),
                    'nom': user.nom,
                    'prenom': user.prenom,
                    'email': user.email,
                    'role': user.role,
                    'is_first_login': user.is_first_login
                },
                'dashboard_url': dashboard_url
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Email/téléphone ou mot de passe incorrect'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur interne: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def logout_api(request):
    """API de déconnexion"""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Déconnexion réussie'
    })


@csrf_exempt
@require_http_methods(["POST"])
def add_user_api(request):
    """API pour ajouter un nouvel utilisateur (admin uniquement)"""
    try:
        # Vérifier que l'utilisateur connecté est admin
        if not request.user.is_authenticated or request.user.role != 'admin':
            return JsonResponse({
                'success': False,
                'message': 'Accès non autorisé. Admin requis.'
            }, status=403)
        
        data = json.loads(request.body)
        
        # Vérifier les champs requis
        required_fields = ['nom', 'prenom', 'email', 'telephone', 'role']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return JsonResponse({
                'success': False,
                'message': f'Champs manquants: {", ".join(missing_fields)}'
            }, status=400)
        
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'message': 'Un utilisateur avec cet email existe déjà'
            }, status=400)
            
        if User.objects.filter(telephone=data['telephone']).exists():
            return JsonResponse({
                'success': False,
                'message': 'Un utilisateur avec ce téléphone existe déjà'
            }, status=400)
        
        # Générer un mot de passe temporaire
        temp_password = generate_temp_password()
        
        # Créer l'utilisateur
        user = User.objects.create(
            username=data['email'],
            email=data['email'],
            nom=data['nom'],
            prenom=data['prenom'],
            telephone=data['telephone'],
            role=data['role'],
            adresse=data.get('adresse', ''),
            numero_compteur=data.get('numero_compteur', ''),
            password=make_password(temp_password),
            temp_password=temp_password,
            is_active=True
        )
        
        # Envoyer les informations par email
        email_sent = send_credentials_email(user, temp_password)
        
        return JsonResponse({
            'success': True,
            'message': f'Utilisateur {user.get_full_name()} créé avec succès',
            'user': {
                'id': str(user.id),
                'nom': user.nom,
                'prenom': user.prenom,
                'email': user.email,
                'role': user.role,
                'temp_password': temp_password
            },
            'email_sent': email_sent
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur interne: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_credentials_api(request):
    """API pour renvoyer les informations de connexion par email"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Email requis'
            }, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }, status=404)
        
        # Générer un nouveau mot de passe temporaire si nécessaire
        if not user.temp_password:
            temp_password = generate_temp_password()
            user.temp_password = temp_password
            user.password = make_password(temp_password)
            user.is_first_login = True
            user.save()
        else:
            temp_password = user.temp_password
        
        # Envoyer l'email
        email_sent = send_credentials_email(user, temp_password)
        
        return JsonResponse({
            'success': True,
            'message': f'Informations de connexion envoyées à {email}',
            'email_sent': email_sent
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Format JSON invalide'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Erreur interne: {str(e)}'
        }, status=500)


@require_http_methods(["GET"])
def dashboard_view(request):
    """Vue simple du dashboard"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Utilisateur non connecté'
        }, status=401)
    
    return JsonResponse({
        'success': True,
        'message': f'Bienvenue sur votre dashboard, {request.user.get_full_name()}!',
        'user': {
            'nom': request.user.nom,
            'prenom': request.user.prenom,
            'role': request.user.role,
            'email': request.user.email
        }
    })


@require_http_methods(["GET"])
def dashboard_stats_view(request):
    """Vue des statistiques générales du dashboard"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Utilisateur non connecté'
        }, status=401)
    
    # Statistiques selon le rôle
    stats = {}
    
    if request.user.role in ['admin', 'superviseur']:
        # Statistiques pour admin/superviseur
        stats = {
            'total_users': User.objects.count(),
            'total_clients': User.objects.filter(role='client').count(),
            'total_techniciens': User.objects.filter(role='technicien').count(),
            'total_categories': Categories.objects.count(),
            'total_reclamations': Reclamation.objects.count(),
            'reclamations_en_attente': Reclamation.objects.filter(status='en_attente').count(),
            'reclamations_en_cours': Reclamation.objects.filter(status='en_cours').count(),
            'reclamations_resolues': Reclamation.objects.filter(status='resolu').count(),
        }
    elif request.user.role == 'client':
        # Statistiques pour client
        stats = {
            'mes_reclamations': Reclamation.objects.filter(user=request.user).count(),
            'en_attente': Reclamation.objects.filter(user=request.user, status='en_attente').count(),
            'en_cours': Reclamation.objects.filter(user=request.user, status='en_cours').count(),
            'resolues': Reclamation.objects.filter(user=request.user, status='resolu').count(),
        }
    elif request.user.role == 'technicien':
        # Statistiques pour technicien
        stats = {
            'reclamations_assignees': Reclamation.objects.filter(technicien=request.user).count(),
            'en_cours': Reclamation.objects.filter(technicien=request.user, status='en_cours').count(),
            'resolues': Reclamation.objects.filter(technicien=request.user, status='resolu').count(),
        }
    
    return JsonResponse({
        'success': True,
        'message': f'Statistiques pour {request.user.get_full_name()}',
        'user_role': request.user.role,
        'statistics': stats
    })


def home_view(request):
    """Vue d'accueil simple"""
    return JsonResponse({
        'message': 'Bienvenue sur l\'API SENELEC',
        'endpoints': {
            'login': '/api/login/',
            'logout': '/api/logout/',
            'add_user': '/api/add-user/',
            'send_credentials': '/api/send-credentials/',
            'dashboard': '/api/dashboard/',
            'dashboard_stats': '/api/dashboard/statistiques-generales/'
        }
    })
