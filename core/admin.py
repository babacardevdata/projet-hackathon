from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Categories, Reclamation


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User
    """
    list_display = ['email', 'nom', 'prenom', 'telephone', 'role', 'is_active', 'date_created']
    list_filter = ['role', 'is_active', 'is_first_login', 'date_created']
    search_fields = ['email', 'nom', 'prenom', 'telephone', 'numero_compteur']
    ordering = ['-date_created']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations Personnelles', {
            'fields': ('nom', 'prenom', 'email', 'telephone', 'adresse', 'numero_compteur')
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Authentification', {
            'fields': ('is_first_login', 'temp_password', 'last_login', 'date_joined'),
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'nom', 'prenom', 'telephone', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Categories
    """
    list_display = ['nom', 'description', 'is_active', 'date_created']
    list_filter = ['is_active', 'date_created']
    search_fields = ['nom', 'description']
    ordering = ['nom']
    
    fieldsets = (
        (None, {
            'fields': ('nom', 'description', 'is_active')
        }),
    )


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    """
    Administration pour le modèle Reclamation
    """
    list_display = ['get_reclamation_id', 'user', 'categories', 'status', 'technicien', 'date_created']
    list_filter = ['status', 'categories', 'date_created', 'dateReponse']
    search_fields = ['user__nom', 'user__prenom', 'user__email', 'description']
    ordering = ['-date_created']
    raw_id_fields = ['user', 'technicien']
    
    fieldsets = (
        ('Informations de la Réclamation', {
            'fields': ('user', 'categories', 'description', 'image')
        }),
        ('Traitement', {
            'fields': ('status', 'technicien', 'dateReponse')
        }),
        ('Métadonnées', {
            'fields': ('date_created', 'date_updated'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['date_created', 'date_updated']
    
    def get_reclamation_id(self, obj):
        return f"#{str(obj.id)[:8]}"
    get_reclamation_id.short_description = 'ID'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'categories', 'technicien')


# Configuration de l'administration
admin.site.site_header = "Administration SENELEC"
admin.site.site_title = "SENELEC Admin"
admin.site.index_title = "Bienvenue dans l'administration SENELEC"
