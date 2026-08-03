"""
Middleware de détection du tenant par hostname.
Attache `request.organization` à chaque requête et expose un contexte thread-local
pour les managers/querysets qui en ont besoin.
"""
import threading

from django.core.exceptions import DisallowedHost
from django.shortcuts import redirect
from django.conf import settings

from .models import Domain, OrganizationUser


# Thread-local pour accéder à l'organisation courante hors des vues (managers, tâches, etc.)
_thread_local = threading.local()


def set_current_organization(organization):
    _thread_local.organization = organization


def get_current_organization():
    return getattr(_thread_local, 'organization', None)


def clear_current_organization():
    _thread_local.organization = None


class TenantMiddleware:
    """
    Détecte l'organisation à partir du domaine de la requête.
    Si le domaine n'est pas reconnu, tente de récupérer l'organisation unique
    de l'utilisateur authentifié. Sinon, organisation = None.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        organization = self.resolve_organization(request)
        request.organization = organization
        set_current_organization(organization)

        response = self.get_response(request)

        clear_current_organization()
        return response

    def resolve_organization(self, request):
        host = request.get_host().split(':')[0].lower()

        # 1. Recherche par domaine exact
        try:
            domain = Domain.objects.select_related('organization').get(
                domain=host, is_active=True, organization__is_active=True
            )
            return domain.organization
        except Domain.DoesNotExist:
            pass

        # 2. Fallback : utilisateur authentifié avec une seule organisation active
        if request.user.is_authenticated:
            memberships = OrganizationUser.objects.filter(
                user=request.user,
                organization__is_active=True
            ).select_related('organization')
            if memberships.count() == 1:
                return memberships.first().organization

        return None


class TenantEnforcementMiddleware:
    """
    Optionnel : redirige vers le portail central si aucun tenant n'est résolu.
    À placer après TenantMiddleware et AuthenticationMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not getattr(request, 'organization', None):
            central_domain = getattr(settings, 'SAAS_CENTRAL_DOMAIN', None)
            if central_domain and central_domain != request.get_host().split(':')[0].lower():
                # On ne redirige pas les requêtes API pour éviter de casser les clients
                if not request.path.startswith('/api/'):
                    return redirect(f"https://{central_domain}{request.path}")
        return self.get_response(request)
