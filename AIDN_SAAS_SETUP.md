# AIDN SaaS - Mise en place

Ce document décrit la transformation du projet AIDN en plateforme SaaS multi-tenant, suite au déplacement des applications `core`, `planning`, `strategy` et `academy` depuis le projet DPSE historique.

## Structure du projet

```
c:\Users\cyril\aidn\
├── mysite/               # Configuration Django
├── general/              # Site public AIDN (déjà présent)
├── users/                # Modèle User custom SaaS
├── core/                 # SaaS core (Organization, Domain, OrganizationUser, middleware)
├── planning/             # Application planning (transférée depuis DPSE)
├── strategy/             # Module stratégique GAR (vide / tenant-ready)
└── academy/              # Module formation et certifications (vide / tenant-ready)
```

## Modèle User

- `AUTH_USER_MODEL = 'users.User'`
- `email` comme identifiant de connexion
- Champs métiers conservés depuis DPSE : `role`, `phone_number`, `photo`, `program`, `entity`, `function`, `profession`, `interest`
- Lien multi-tenant : `organizations` via `core.OrganizationUser`

## Modèles SaaS

- `core.Organization` : tenant/client
- `core.Domain` : domaine pointant vers une organisation
- `core.OrganizationUser` : rôle SaaS d'un utilisateur dans une organisation
- `core.TenantModel` : mixin abstrait pour isoler les données par organisation

## Middleware et contexte

- `core.middleware.TenantMiddleware` : résout `request.organization` à partir du hostname ou de l'appartenance unique de l'utilisateur.
- `core.context_processors.organization` : expose `organization` dans tous les templates.

## Configuration requise

Variables à positionner dans le `.env` de production :

```env
ALLOWED_HOSTS=localhost,127.0.0.1,app.aidn.ci,dpse.aidn.ci,dpse.mfb.gouv.ci
CSRF_TRUSTED_ORIGINS=https://*.aidn.ci,https://*.mfb.gouv.ci
SAAS_CENTRAL_DOMAIN=app.aidn.ci
DATABASE_URL=mysql://user:pass@host:3306/dpse_db
```

## Dépendances

`requirements.txt` inclut désormais :

- `mysqlclient` : connexion à la base DPSE (MySQL)
- `Pillow` : champ `photo` du modèle User
- `django-filter` : filtres dans planning
- `celery`, `django-celery-beat`, `django-celery-results` : tâches asynchrones
- `redis` : broker Celery

## Routes ajoutées

- `/planning/` : application planning
- `/strategie/` : module stratégique
- `/academy/` : module academy
- `/admin/` : administration
- `/` : site public AIDN

## Migrations

Ordre recommandé :

```bash
python manage.py migrate users
python manage.py migrate core
python manage.py migrate planning
python manage.py migrate strategy
python manage.py migrate academy
```

La migration `core/0002_seed_dpse_organization.py` crée automatiquement l'organisation DPSE et rattache tous les utilisateurs existants.

## Prochaines étapes

1. **Connexion base de données** : basculer AIDN de SQLite vers la base MySQL de DPSE (même schéma, mêmes données).
2. **Alignement Django** : passer AIDN en Django 5.2.10 pour correspondre à DPSE.
3. **Déploiement domaines** : faire pointer `app.aidn.ci`, `dpse.aidn.ci` et `dpse.mfb.gouv.ci` vers l'application AIDN.
4. **Tests d'isolation** : vérifier que chaque organisation ne voit que ses propres données.
5. **Page de sélection d'organisation** : pour les utilisateurs multi-tenant.
6. **Celery** : déjà configuré avec Redis ; vérifier les tâches asynchrones de planning.

## Docker / Celery

Le `docker-compose.yml` contient désormais :

- `web` : application Django
- `db` : PostgreSQL (peut être remplacé par MySQL)
- `redis` : broker Celery
- `celery_worker` : exécution des tâches asynchrones
- `celery_beat` : planification des tâches périodiques

Fichiers ajoutés : `@c:\Users\cyril\aidn\mysite\celery.py` et mise à jour de `@c:\Users\cyril\aidn\mysite\__init__.py`.

## Risques

- Le projet AIDN était initialement en SQLite/PostgreSQL. Le passage à MySQL doit être testé sur une copie de la base.
- `planning` importe `celery`. Il faut installer les dépendances listées avant de lancer le serveur.
- Les templates et vues de planning peuvent contenir des liens absolus vers l'ancien domaine DPSE ; il faudra les vérifier.
