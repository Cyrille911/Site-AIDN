from celery import shared_task
from planning.models import Activite, Organization
from planning.utils import organization_context

@shared_task
def check_activity_alerts_task():
    """Lance les alertes pour chaque organisation active, en isolation."""
    for organization in Organization.objects.filter(is_active=True):
        with organization_context(organization.id) as org:
            if org:
                Activite.check_activity_alerts(organization=org)