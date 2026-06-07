# SekhmetKarnark — Accès & Identifiants

## Production (Railway)

**URL :** https://web-production-83971.up.railway.app/

### Administration Django
- **URL :** https://web-production-83971.up.railway.app/admin/
- **Utilisateur :** `admin`
- **Mot de passe :** `Admin0002!`

### Base de données (Railway)
- PostgreSQL hébergé par Railway (accès via `railway variable list`)

### Services
- **Redis :** redis://redis.railway.internal:6379
- **Cache :** Redis (via django-redis)

---

## Local (Développement)

```bash
# Lancer le serveur
python manage.py runserver
```

- **URL :** http://localhost:8000/
- **Admin :** http://localhost:8000/admin/
- **Identifiants :** `admin` / `Admin0002!`

### Base de données locale
- **Engine :** PostgreSQL
- **Base :** `sekhmetkarnak`
- **Utilisateur :** `postgres`
- **Mot de passe :** `Pain0002`
- **Hôte :** `localhost:5432`

---

## Réinitialisation du mot de passe admin

```bash
python manage.py changepassword admin
```

## Seed des données de démo

```bash
python manage.py seed_data
```

Cela crée :
- **5 produits** (Néroli Impérial, Ashwagandha Sombre, etc.)
- **6 articles de blog**
- **5 catégories boutique** + **3 catégories blog** + **5 tags**
