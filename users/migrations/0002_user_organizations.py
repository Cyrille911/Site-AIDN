# Generated manually: add organizations M2M through planning.OrganizationUser

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('planning', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(
                    model_name='user',
                    name='organizations',
                    field=models.ManyToManyField(
                        blank=True,
                        related_name='users',
                        through='planning.OrganizationUser',
                        to='planning.organization',
                        verbose_name='Organisations',
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
