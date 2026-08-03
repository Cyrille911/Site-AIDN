from django.urls import path
from . import views

urlpatterns = [
    # Accueil
    path('', views.accueil, name='accueil'),
    path('contact/', views.contact_email, name='contact_email'),
    path('nos-produits/', views.nos_produits, name='nos_produits'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('nous-joindre/', views.nous_joindre, name='nous_joindre'),
    path('voir-plus/', views.voir_plus, name='voir_plus'),
]
