# L'organisation seedée par 0002 portait le nom et les domaines de DPSE,
# qui est un site distinct. On la renomme AIDN et on remplace ses domaines.

from django.db import migrations, models


def forwards(apps, schema_editor):
    Organization = apps.get_model('planning', 'Organization')
    Domain = apps.get_model('planning', 'Domain')

    org = Organization.objects.filter(slug='dpse').first() or Organization.objects.filter(slug='aidn').first()
    if org is None:
        return
    org.slug = 'aidn'
    org.name = 'Agence Ivoirienne de Développement Numérique (AIDN)'
    org.description = 'Organisation principale de la plateforme AIDN.'
    org.branding = {**(org.branding or {}), 'display_name': 'AIDN'}
    org.save()

    Domain.objects.filter(organization=org).exclude(domain__in=['aidn.ci', 'www.aidn.ci']).delete()
    Domain.objects.update_or_create(domain='aidn.ci', defaults={'organization': org, 'is_primary': True, 'is_active': True})
    Domain.objects.update_or_create(domain='www.aidn.ci', defaults={'organization': org, 'is_primary': False, 'is_active': True})


def backwards(apps, schema_editor):
    Organization = apps.get_model('planning', 'Organization')
    Domain = apps.get_model('planning', 'Domain')
    org = Organization.objects.filter(slug='aidn').first()
    if org is None:
        return
    org.slug = 'dpse'
    org.name = 'Direction de la Planification et du Suivi-Évaluation (DPSE)'
    org.branding = {**(org.branding or {}), 'display_name': 'DPSE'}
    org.save()
    Domain.objects.filter(organization=org).delete()
    Domain.objects.create(domain='dpse.aidn.ci', organization=org, is_primary=True, is_active=True)


class Migration(migrations.Migration):

    dependencies = [
        ('planning', '0008_domain_help_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='domain',
            field=models.CharField(db_index=True, help_text='Exemple : aidn.ci ou app.aidn.ci', max_length=253, unique=True, verbose_name='Domaine'),
        ),
        migrations.RunPython(forwards, backwards),
    ]
