"""
Managers et querysets pour l'isolation des données par organisation.

Approche retenue : pas de filtrage magique global (trop risqué en production).
Chaque modèle tenant expose :
- objects : manager Django standard (tous les tenants, admin/tasks)
- tenant_objects : manager qui filtre par l'organisation courante (thread-local/request)
- for_organization(org) : helper explicite
"""
from django.db import models

from .middleware import get_current_organization


class TenantQuerySet(models.QuerySet):
    def for_organization(self, organization):
        return self.filter(organization=organization)

    def for_current_organization(self):
        org = get_current_organization()
        if org:
            return self.for_organization(org)
        return self.none()


class TenantManager(models.Manager):
    _queryset_class = TenantQuerySet

    def get_queryset(self):
        return super().get_queryset()

    def for_organization(self, organization):
        return self.get_queryset().for_organization(organization)

    def for_current_organization(self):
        return self.get_queryset().for_current_organization()


class ScopedTenantManager(TenantManager):
    """
    Manager qui, par défaut, filtre automatiquement sur l'organisation courante.
    Utile pour les vues et les templates. À utiliser avec précaution dans l'admin
    ou les tâches asynchrones : préférer `objects` ou `for_organization()`.
    """

    def get_queryset(self):
        qs = super().get_queryset()
        org = get_current_organization()
        if org:
            return qs.filter(organization=org)
        return qs
