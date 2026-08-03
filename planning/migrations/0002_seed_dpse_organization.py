# Generated manually: create DPSE organization and link all existing users.

from django.db import migrations
from django.conf import settings


def create_dpse_organization(apps, schema_editor):
    Organization = apps.get_model('planning', 'Organization')
    Domain = apps.get_model('planning', 'Domain')
    OrganizationUser = apps.get_model('planning', 'OrganizationUser')
    User = apps.get_model(settings.AUTH_USER_MODEL.split('.')[0], settings.AUTH_USER_MODEL.split('.')[1])

    dpse, _ = Organization.objects.get_or_create(
        slug='dpse',
        defaults={
            'name': 'Direction de la Planification et du Suivi-Évaluation (DPSE)',
            'description': 'Organisation cliente initiale et données historiques.',
            'status': 'active',
            'is_active': True,
            'branding': {
                'display_name': 'DPSE',
                'primary_color': '#0056b3',
            },
        }
    )

    # Domaines associés à DPSE
    domains = ['dpse.aidn.ci', 'dpse.mfb.gouv.ci']
    for idx, domain_name in enumerate(domains):
        Domain.objects.get_or_create(
            domain=domain_name,
            defaults={
                'organization': dpse,
                'is_primary': idx == 0,
                'is_active': True,
            }
        )

    # Attache tous les utilisateurs existants à DPSE en tant qu'admin_org
    # pour préserver leurs droits historiques. À affiner manuellement ensuite.
    for user in User.objects.all():
        OrganizationUser.objects.get_or_create(
            user=user,
            organization=dpse,
            defaults={
                'role': 'admin_org',
                'is_admin': True,
                'job_title': 'Membre historique DPSE',
            }
        )


def reverse_dpse_organization(apps, schema_editor):
    Organization = apps.get_model('planning', 'Organization')
    Organization.objects.filter(slug='dpse').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0001_initial'),
        # S'assurer que les utilisateurs existent avant de les lier
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_dpse_organization, reverse_dpse_organization),
    ]
