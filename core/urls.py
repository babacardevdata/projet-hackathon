from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # API d'authentification
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    
    # API de gestion des utilisateurs
    path('api/add-user/', views.add_user_api, name='add_user_api'),
    path('api/send-credentials/', views.send_credentials_api, name='send_credentials_api'),
    
    # Dashboard
    path('api/dashboard/', views.dashboard_view, name='dashboard'),
    path('api/dashboard/statistiques-generales/', views.dashboard_stats_view, name='dashboard_stats'),
    
    # Page d'accueil
    path('', views.home_view, name='home'),
] 