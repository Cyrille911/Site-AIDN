# Guide de Déploiement - Site AIDN sur VPS LWS

## Prérequis sur le VPS
- Docker installé
- Docker Compose installé
- Git installé (optionnel)

## Étapes de déploiement

### 1. Connexion au VPS
```bash
ssh user@VOTRE_IP_VPS
```

### 2. Cloner ou transférer le projet
**Option A - Via Git :**
```bash
git clone https://github.com/VOTRE_REPO/Site-AIDN.git
cd Site-AIDN
```

**Option B - Via SCP (depuis votre machine locale) :**
```bash
# Depuis votre machine Windows (PowerShell)
scp -r D:\DEVS\Site-AIDN user@VOTRE_IP_VPS:/home/user/
```

### 3. Créer le fichier .env
```bash
cd Site-AIDN
cp env.template .env
nano .env
```

Modifier les valeurs :
```env
DEBUG=0
SECRET_KEY=votre-cle-secrete-unique-et-longue
ALLOWED_HOSTS=votre-domaine.com,VOTRE_IP_VPS

POSTGRES_DB=aidn_db
POSTGRES_USER=aidn_user
POSTGRES_PASSWORD=mot-de-passe-securise

DB_HOST=db
DB_PORT=5432
```

**Générer une SECRET_KEY sécurisée :**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 4. Lancer le déploiement
```bash
chmod +x deploy.sh
./deploy.sh
```

**Ou manuellement :**
```bash
docker-compose up -d --build
```

### 5. Créer un superuser (optionnel)
```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Vérifier le statut
```bash
docker-compose ps
docker-compose logs -f
```

## Accès à l'application
- **Sans domaine** : http://VOTRE_IP_VPS
- **Avec domaine** : http://votre-domaine.com

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `docker-compose ps` | Voir les conteneurs |
| `docker-compose logs -f` | Voir les logs en temps réel |
| `docker-compose down` | Arrêter les conteneurs |
| `docker-compose restart` | Redémarrer |
| `docker-compose exec web bash` | Shell dans le conteneur |

## Configuration HTTPS (recommandé)

Pour activer HTTPS avec Let's Encrypt, ajoutez Certbot :

```bash
# Installer certbot sur le VPS
sudo apt install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com
```

## Base de données

Django utilise **PostgreSQL** (conteneur `db`) dès que `DB_HOST` est défini
dans `.env`. Sans `DB_HOST` (dev sans Docker), il retombe sur SQLite
(`db.sqlite3`, non versionné).

Sauvegarde / restauration :
```bash
docker-compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql
docker-compose exec -T db psql -U $POSTGRES_USER $POSTGRES_DB < backup.sql
```

## Modifier le fichier .env

Après toute modification du `.env` (mot de passe SMTP, etc.), `restart` ne
suffit pas : les variables ne sont relues qu'à la recréation du conteneur.

```bash
docker-compose up -d --force-recreate web
```

## Mise à jour de l'application

```bash
cd Site-AIDN
git pull origin main
./deploy.sh
```

## Troubleshooting

**Erreur de connexion à la base de données :**
```bash
docker-compose logs db
docker-compose restart db
```

**Erreur de permissions :**
```bash
sudo chown -R $USER:$USER .
chmod +x deploy.sh entrypoint.sh
```

**Reconstruire complètement :**
```bash
docker-compose down -v
docker-compose up -d --build
```
