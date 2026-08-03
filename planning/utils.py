"""
Utilitaires multi-tenant.
"""
from django.core.exceptions import PermissionDenied

from .middleware import get_current_organization
from .models import Organization


def get_organization_from_request(request):
    """Retourne l'organisation attachée à la requête, ou None."""
    return getattr(request, 'organization', None)


def require_organization(request):
    """Lève PermissionDenied si aucune organisation n'est résolue."""
    org = get_organization_from_request(request)
    if not org:
        raise PermissionDenied("Aucune organisation associée à cette requête.")
    return org


def organization_context(organization_id):
    """
    Context manager pour exécuter du code dans le contexte d'une organisation
    donnée (tâches Celery, commandes management, etc.).
    """
    from .middleware import set_current_organization, clear_current_organization

    class OrgContext:
        def __init__(self, org_id):
            self.org_id = org_id
            self.org = None

        def __enter__(self):
            if self.org_id:
                try:
                    self.org = Organization.objects.get(pk=self.org_id)
                except Organization.DoesNotExist:
                    self.org = None
            set_current_organization(self.org)
            return self.org

        def __exit__(self, exc_type, exc_val, exc_tb):
            clear_current_organization()
            return False

    return OrgContext(organization_id)
