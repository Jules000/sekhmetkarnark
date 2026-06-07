# Session Context — SekhmetKarnark

**Last session :** 07 Juin 2026
**Status :** À reprendre

---

## ✅ Accompli (3 sprints)

### Sprint 1 — Structure Django + Templates
- Projet Django 5.1 complet (122 fichiers, 10 apps)
- 26 templates HTML intégrés depuis templates Stitch (design préservé)
- 3 environnements (base, local, production)
- Cache Redis multi-niveaux avec invalidation
- Architecture offline-first (Tailwind local, @font-face)
- Dockerfile + railway.toml

### Sprint 2 — Infrastructure & Tests
- Environnement virtuel + 25+ dépendances installées
- 33 polices Google Fonts (woff2) téléchargées dans `static/fonts/`
- 18 images des templates copiées dans `static/images/`
- PostgreSQL configuré, 32 migrations appliquées
- 13 tests unitaires (100% OK)
- CI/CD GitHub Actions (.github/workflows/deploy.yml)
- Fix compatibilité Python 3.14 (patch django context)

### Sprint 3 — Seed Data & Déploiement
- 5 produits, 6 articles, catégories, tags (identiques aux templates)
- Management command `python manage.py seed_data`
- Déploiement Railway réussi
- Services : PostgreSQL + Redis en ligne
- Variables d'environnement configurées sur le web service

---

## 🚀 Infrastructure Railway

**Projet :** sekhmetkarnark
**URL :** https://web-production-83971.up.railway.app/
**Admin :** https://web-production-83971.up.railway.app/admin/
**Identifiants :** admin / Admin0002!

**Services :**
- **web** (Dockerfile) → Online
- **Postgres** → Online  
- **redis** → Online

**Variables d'env (web service) :**
- `DATABASE_URL` → ${{Postgres.DATABASE_URL}}
- `REDIS_URL` → redis://redis.railway.internal:6379
- `DJANGO_SETTINGS_MODULE` → config.settings.production
- `DEBUG` → False
- `ALLOWED_HOSTS` → .railway.app .up.railway.app healthcheck.railway.app
- `SECRET_KEY` → django-insecure-railway-key

---

## 📁 Structure du Projet

```
G:\sekhmetkarnark\
├── Templates\              # Templates Stitch originaux (non modifiés)
├── sekhmetkarnark\         # Projet Django (git repo)
│   ├── config/settings/    # base.py, local.py, production.py
│   ├── apps/               # 10 apps Django
│   │   ├── core/           # Pages statiques, cache_config, seed_data
│   │   ├── accounts/       # Auth custom User, profils, OTP
│   │   ├── blog/           # Articles, catégories, tags
│   │   ├── shop/           # Produits, catégories, images
│   │   ├── cart/           # Panier session
│   │   ├── orders/         # Commandes, checkout
│   │   ├── payments/       # Webhook Tranzak
│   │   ├── newsletter/     # Double opt-in
│   │   ├── contact/        # Messages
│   │   └── seo/            # Robots, Sitemap
│   ├── templates/          # 26 templates Django
│   ├── static/             # CSS, fonts (33 woff2), images (18), icons
│   ├── locale/             # FR/EN (à remplir)
│   ├── requirements/       # base.txt, local.txt, production.txt
│   ├── scripts/            # download_fonts, generate_fonts_css, etc.
│   ├── .github/workflows/  # CI/CD
│   ├── Dockerfile
│   ├── railway.toml
│   ├── .env (local)
│   ├── ADMIN_CREDENTIALS.md
│   ├── SESSION_CONTEXT.md
│   ├── sprint-001-initialisation-django.md
│   └── sprint-002-infrastructure-tests.md
├── sprint-001-initialisation-django.md
└── sprint-002-infrastructure-tests.md
```

---

## 🔜 Prochaines étapes (à reprendre)

### Priorité Haute
1. **Domaine personnalisé** sur Railway
2. **Pipeline CI/CD GitHub Actions** finaliser (nécessite RAILWAY_TOKEN)
3. **Images produits** upload via l'admin Django
4. **Tests** supplémentaires (shop, cart, orders, blog detail)
5. **Traductions** FR/EN (fichiers .po dans locale/)

### Priorité Moyenne
6. **Paiement Tranzak** (configurer webhook)
7. **Newsletter Brevo** (configurer API)
8. **Plan du site** / sitemap.xml dynamique
9. **Recherche** avec django-filter
10. **Mode sombre** (dark mode déjà supporté dans tailwind.config)

### Backlog
11. **Monitoring** Sentry
12. **Sécurité** CSP, rate limiting, MFA
13. **Images responsives** avec AVIF/WEBP via django-imagekit

---

## Commandes Utiles

```bash
# Local
cd G:\sekhmetkarnark\sekhmetkarnark
.venv\Scripts\Activate.ps1
python manage.py seed_data
python manage.py runserver

# Railway
railway up --service web --path-as-root "G:\sekhmetkarnark\sekhmetkarnark"
railway logs -s web
railway variable list -s web --json

# Git
git add -A && git commit -m "message" && git push
```

## Problèmes Connus

- **Déploiement Railway** nécessite `--path-as-root` pour utiliser le bon dossier racine
- **ALLOWED_HOSTS** doit contenir `healthcheck.railway.app` pour le healthcheck
- **Python 3.14** nécessite patch de `django/template/context.py` pour `__copy__`
- **Redis** non disponible en local → fallback LocMemCache automatique
- **SECURE_SSL_REDIRECT** désactivé (géré par Railway edge)
