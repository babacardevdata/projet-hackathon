from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import uuid


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour le système SENELEC
    """
    ROLE_CHOICES = [
        ('admin', 'Administrateur'),
        ('superviseur', 'Superviseur'), 
        ('client', 'Client'),
        ('technicien', 'Technicien'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15, unique=True, db_index=True)
    adresse = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='client')
    numero_compteur = models.CharField(max_length=30, blank=True, null=True)
    
    # Champs pour l'authentification automatique
    is_first_login = models.BooleanField(default=True)
    temp_password = models.CharField(max_length=20, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nom', 'prenom', 'telephone']
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        db_table = 'core_user'
    
    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.role})"
    
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


class Categories(models.Model):
    """
    Modèle pour les catégories de réclamations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        db_table = 'core_categories'
    
    def __str__(self):
        return self.nom


class Reclamation(models.Model):
    """
    Modèle pour les réclamations des clients
    """
    STATUS_CHOICES = [
        ('en_attente', 'En Attente'),
        ('en_cours', 'En Cours'),
        ('resolu', 'Résolu'),
        ('ferme', 'Fermé'),
        ('annule', 'Annulé'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='en_attente')
    dateReponse = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='reclamations/', blank=True, null=True)
    
    # Relations
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reclamations')
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='reclamations')
    technicien = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name='reclamations_assignees',
        limit_choices_to={'role': 'technicien'}
    )
    
    # Champs de traçabilité
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Réclamation'
        verbose_name_plural = 'Réclamations'
        ordering = ['-date_created']
        db_table = 'core_reclamation'
    
    def __str__(self):
        return f"Réclamation #{str(self.id)[:8]} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Automatiquement définir dateReponse quand le status change vers 'resolu' ou 'ferme'
        if self.status in ['resolu', 'ferme'] and not self.dateReponse:
            self.dateReponse = timezone.now()
        super().save(*args, **kwargs)
