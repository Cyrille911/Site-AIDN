# Plan de fusion : academy + core + planning -> planning

## Objectif

- Créer une seule app Django `planning` contenant les modèles de `core`, `academy` et l'ancien `planning`.
- Renommer l'ancien app `planning` (données opérationnelles) en `monitoring`.
- Supprimer les apps `core` et `academy`.
- Mettre à jour `settings.py`, `urls.py` et tous les imports.

## Structure cible

```
c:\Users\cyril\aidn\
├── planning/                 # App fusionnée
│   ├── models.py             # Organization, Domain, OrganizationUser, TenantModel
│   │                           # TrainingCourse, Certification
│   │                           # PlanAction, Effet, Produit, Action, Activite, ActiviteLog
│   ├── middleware.py         # TenantMiddleware
│   ├── context_processors.py   # organization
│   ├── managers.py
│   ├── signals.py
│   ├── utils.py
│   ├── admin.py
│   ├── views.py              # Vues de l'ancien planning + academy
│   ├── urls.py
│   ├── forms.py
│   ├── templates/
│   │   ├── planning/           # Templates de l'ancien planning
│   │   └── academy/            # Templates de academy
│   └── migrations/
│       ├── 0001_initial.py     # Tous les modèles fusionnés
│       └── 0002_seed_dpse_organization.py
├── monitoring/               # Ancien planning renommé
│   ├── apps.py                 # name = 'monitoring'
│   ├── views.py                # Vues de suivi/exécution utilisant les modèles de planning
│   ├── urls.py
│   └── templates/monitoring/
└── users/                    # App users (inchangée, mais imports mis à jour)
```

## Étapes techniques

1. **Renommer `planning` en `monitoring`**
   - Déplacer le dossier `planning` vers `monitoring`.
   - Créer `monitoring/apps.py` avec `name = 'monitoring'` et `verbose_name = 'Monitoring'`.
   - Créer une migration de renommage de toutes les tables `planning_*` vers `monitoring_*`.
   - Supprimer les modèles de `monitoring` (les données sont dans les tables renommées, mais les modèles vivent maintenant dans `planning`).

2. **Créer la nouvelle app `planning`**
   - Créer le dossier `planning`.
   - Copier les modèles de `core` et `academy`.
   - Copier les modèles de l'ancien planning (dans `monitoring`) avec leurs champs exacts.
   - Fusionner les dépendances (surtout `Organization` et `User`).
   - Créer `planning/migrations/0001_initial.py` avec tous les modèles.
   - Créer `planning/migrations/0002_seed_dpse_organization.py`.

3. **Mettre à jour les imports**
   - Remplacer `from core.models import ...` par `from planning.models import ...`.
   - Remplacer `from core.middleware import ...` par `from planning.middleware import ...`.
   - Remplacer `from core.context_processors import ...` par `from planning.context_processors import ...`.
   - Remplacer `from academy.models import ...` par `from planning.models import ...`.
   - Remplacer `from planning.models import ...` (dans monitoring) par `from planning.models import ...` (même nom, mais modèles dans la nouvelle app).

4. **Supprimer les anciennes apps**
   - Supprimer `core` et `academy`.

5. **Mettre à jour `settings.py`**
   - Remplacer `'core.apps.CoreConfig'` par `'planning.apps.PlanningConfig'`.
   - Remplacer `'academy.apps.AcademyConfig'` par `'planning.apps.PlanningConfig'` (attention aux doublons).
   - Remplacer `'planning.apps.PlanningConfig'` par `'monitoring.apps.MonitoringConfig'`.
   - Mettre à jour `MIDDLEWARE` : `planning.middleware.TenantMiddleware`.
   - Mettre à jour `TEMPLATES` : `planning.context_processors.organization`.

6. **Mettre à jour `urls.py`**
   - `path('planning/', include('planning.urls'))` pour la nouvelle app.
   - `path('monitoring/', include('monitoring.urls'))` pour monitoring.
   - Supprimer `path('academy/', include('academy.urls'))`.

7. **Mettre à jour les templates**
   - Déplacer les templates de `monitoring/templates/planning/` vers `monitoring/templates/monitoring/`.
   - Copier les templates de `academy/templates/academy/` vers `planning/templates/academy/`.
   - Copier les templates de `monitoring/templates/planning/` vers `planning/templates/planning/`.

## Risques

- **Perte de données** : si les migrations de renommage de tables sont mal faites, les données de l'ancien planning peuvent être perdues.
- **Conflits de migrations** : Django peut refuser d'appliquer les migrations si des tables existent déjà.
- **Références cyclées** : `users.User` dépend de `planning.Organization` (via `OrganizationUser`). `planning.OrganizationUser` dépend de `users.User`. Il faut maintenir l'ordre des migrations.
- **Tests** : cette opération doit être testée sur une copie de la base avant de toucher la production.

## Prérequis

- Faire un backup de `c:\Users\cyril\aidn\db.sqlite3` avant de lancer les migrations.
- Exécuter `python manage.py migrate` uniquement après validation de la syntaxe.

## État actuel

- Fusion terminée et migrations appliquées avec succès.
- `planning` contient désormais tout : modèles, vues, templates, URLs, signaux, tâches, filtres de l'ancien `core`, `academy`, `planning`, `monitoring` et `strategy`.
- `strategy`, `monitoring`, `core` et `academy` sont supprimées de `INSTALLED_APPS`, de la base de données et du disque.
- Toutes les tables de données sont renommées en `planning_*`.
- `users.User.organizations` pointe vers `planning.Organization` via `planning.OrganizationUser`.
- Vérifications OK : `manage.py check`, `migrate --plan`, `makemigrations --check`.

## Commandes de vérification

```bash
python manage.py check
python manage.py migrate --plan
python manage.py makemigrations --check
python manage.py runserver 8000
```
